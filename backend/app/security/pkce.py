"""Helpers for Proof Key for Code Exchange (PKCE)."""

import base64
import hashlib
import secrets
from typing import Tuple


def generate_pkce_challenge() -> Tuple[str, str]:
    """
    Generates a PKCE code verifier and a corresponding code challenge.

    Returns:
        A tuple containing (code_verifier, code_challenge).
    """
    # Create a high-entropy cryptographic random string
    code_verifier = secrets.token_urlsafe(64)

    # Hash the verifier using SHA-256
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()

    # Base64url-encode the hash to get the code challenge
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")

    return code_verifier, code_challenge