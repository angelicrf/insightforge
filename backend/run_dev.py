"""
A development script to run the Uvicorn server and an ngrok tunnel simultaneously.
"""
import asyncio
import json
import os
import secrets
from datetime import datetime, timezone
from urllib.parse import quote_plus
import webbrowser

import httpx
import uvicorn
from dotenv import load_dotenv
from ngrok import ngrok

from app.config.settings import settings
from app.security.pkce import generate_pkce_challenge


def _persist_pkce_state(state: str, code_verifier: str, code_challenge: str, redirect_uri: str) -> None:
    """Store PKCE material and redirect URI for callback exchange in local development."""
    payload = {
        "state": state,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "redirect_uri": redirect_uri,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(settings.SALESFORCE_PKCE_CACHE_FILE, "w", encoding="utf-8") as cache_file:
        json.dump(payload, cache_file)


def _persist_token(token_data: dict) -> None:
    """Write Salesforce token response to local cache file."""
    with open(settings.SALESFORCE_TOKEN_FILE, "w", encoding="utf-8") as token_file:
        json.dump(token_data, token_file)


async def _try_client_credentials_token(login_url: str, client_id: str, client_secret: str) -> bool:
    """Try machine-to-machine token retrieval with client credentials grant."""
    token_url = f"{login_url.rstrip('/')}/services/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(token_url, data=payload)

    if response.status_code >= 400:
        print("Client credentials flow not available with current Salesforce settings.")
        print(f"Reason: {response.text}")
        return False

    token_data = response.json()
    _persist_token(token_data)
    print(f"Salesforce access token created and stored at: {settings.SALESFORCE_TOKEN_FILE}")
    return True


async def _start_ngrok_tunnel(port: int, authtoken: str):
    """Start ngrok using reserved domain if available, fallback to ephemeral URL."""
    domain = os.getenv("NGROK_DOMAIN")
    try:
        if domain:
            return await ngrok.forward(port, authtoken=authtoken, domain=domain)
        return await ngrok.forward(port, authtoken=authtoken)
    except ValueError as exc:
        if domain:
            print(f"Warning: failed to use NGROK_DOMAIN '{domain}'. Falling back to random ngrok URL.")
            print(f"Reason: {exc}")
            return await ngrok.forward(port, authtoken=authtoken)
        print("Warning: unable to start ngrok tunnel. Continuing without creating a new tunnel.")
        print(f"Reason: {exc}")
        return None


async def main():
    """
    Starts the FastAPI server and an ngrok tunnel, printing the public URL.
    """
    # Load .env file if it exists, otherwise fall back to .env.example
    if os.path.exists(".env"):
        load_dotenv()
    else:
        load_dotenv(dotenv_path=".env.example")

    authtoken = os.getenv("NGROK_AUTHTOKEN")
    print(f"NGROK_AUTHTOKEN: {authtoken}")  # Debugging line to check if the token is loaded    
    client_id = os.getenv("SALESFORCE_CLIENT_ID")
    client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
    login_url = os.getenv("SALESFORCE_LOGIN_URL", "https://login.salesforce.com")

    if not client_id or not client_secret:
        print("Error: SALESFORCE_CLIENT_ID and SALESFORCE_CLIENT_SECRET are required.")
        return

    grant_mode = os.getenv("SALESFORCE_GRANT_MODE", "auto").lower()
    if grant_mode in {"auto", "client_credentials"}:
        if await _try_client_credentials_token(login_url, client_id, client_secret):
            return
        if grant_mode == "client_credentials":
            print("Stopping because SALESFORCE_GRANT_MODE is set to client_credentials only.")
            return

    if not authtoken:
        print("Error: NGROK_AUTHTOKEN not found in environment variables.")
        print("Please add it to your .env file, or enable client credentials on Salesforce.")
        return

    # Get server port from environment, default to 8000
    port = int(os.getenv("DEV_SERVER_PORT", "8000"))

    # Set up the ngrok tunnel
    listener = await _start_ngrok_tunnel(port, authtoken)
    redirect_uri = os.getenv("SALESFORCE_REDIRECT_URI")
    if listener is not None:
        redirect_uri = f"{listener.url()}/api/v1/integrations/salesforce/oauth/callback"

    if not redirect_uri:
        print("Error: SALESFORCE_REDIRECT_URI is not set and no ngrok tunnel is available.")
        return
    # Generate PKCE challenge for the OAuth flow
    code_verifier, code_challenge = generate_pkce_challenge()
    state = secrets.token_urlsafe(24)
    _persist_pkce_state(state, code_verifier, code_challenge, redirect_uri)

    # Set the verifier as an environment variable for the server process to access.
    # This is a development-only convenience.
    os.environ["DEV_PKCE_CODE_VERIFIER"] = code_verifier

    print("-" * 50)
    print(f"Server running at: http://127.0.0.1:{port}")
    if listener is not None:
        print(f"Ngrok tunnel active at: {listener.url()}")
    else:
        print("Ngrok tunnel active at: (reusing previously configured callback URL)")
    print(f"Salesforce Callback URL: {redirect_uri}")
    print("\nStarting Salesforce OAuth flow automatically in your browser...")
    redirect_uri_encoded = quote_plus(redirect_uri)
    auth_url = (
        f"{login_url}/services/oauth2/authorize?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri_encoded}&state={state}"
        f"&code_challenge={code_challenge}&code_challenge_method=S256"
    )
    print(auth_url)
    open_browser = os.getenv("SALESFORCE_AUTO_OPEN_BROWSER", "true").lower() == "true"
    if open_browser:
        webbrowser.open(auth_url, new=2)
        print("Browser opened automatically. Complete login/consent; callback will exchange token internally.")
    else:
        print("Set SALESFORCE_AUTO_OPEN_BROWSER=true to auto-open this URL.")
    print("\nAfter logging in, you will be redirected back and the token exchange will happen automatically.")
    print("-" * 50)

    # Set up the Uvicorn server
    config = uvicorn.Config("app.main:app", host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)

    # Run the server
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server.")