"""Streamlit frontend for the InsightForge platform."""

from __future__ import annotations

import os

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from audiorecorder import audiorecorder

DEFAULT_BACKEND_URL = "http://127.0.0.1:8000/api/v1/assistant/query"


def render_shell() -> None:
    """Render the primary layout and visual styling."""
    st.set_page_config(
        page_title="InsightForge Control Room",
        page_icon="IF",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 209, 102, 0.18), transparent 28%),
                radial-gradient(circle at bottom right, rgba(76, 201, 240, 0.22), transparent 30%),
                linear-gradient(135deg, #0d1b2a 0%, #12344d 58%, #cb6a38 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero {
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 24px;
            background: rgba(5, 14, 23, 0.68);
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.24);
            color: #f7f5ef;
            margin-bottom: 1rem;
        }
        .eyebrow {
            font-size: 0.8rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #ffd166;
            margin-bottom: 0.6rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 3rem;
            line-height: 1.05;
        }
        .hero p {
            color: #d9e2ec;
            max-width: 52rem;
            font-size: 1.02rem;
        }
        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        .feature-card {
            min-height: 180px;
            padding: 1.1rem;
            border-radius: 20px;
            background: rgba(6, 18, 32, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.14);
        }
        .feature-kicker {
            color: #ffd166;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.78rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_backend_url() -> str:
    """Read the backend URL from secrets or environment."""
    secret_value = None
    try:
        secret_value = st.secrets.get("BACKEND_URL")
    except StreamlitSecretNotFoundError:
        secret_value = None

    url = secret_value or os.getenv("INSIGHTFORGE_BACKEND_URL")
    if not url:
        st.warning(
            "Backend URL not set. Using default local URL. Set `INSIGHTFORGE_BACKEND_URL` or a Streamlit secret `BACKEND_URL`."
        )
        return DEFAULT_BACKEND_URL
    return url


def render_header(active_backend_url: str) -> None:
    """Render the hero section and summary metrics."""
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">InsightForge Platform</div>
            <h1>Turn support traffic into actionable operator context.</h1>
            <p>
                Streamlit now serves as the entire frontend surface for triage, voice capture,
                and backend-assisted response generation.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.markdown(
        "<div class='metric-card'><strong>Frontend stack</strong><br/>Streamlit only</div>",
        unsafe_allow_html=True,
    )
    col2.markdown(
        "<div class='metric-card'><strong>Backend target</strong><br/>FastAPI assistant endpoint</div>",
        unsafe_allow_html=True,
    )
    col3.markdown(
        f"<div class='metric-card'><strong>Current URL</strong><br/>{active_backend_url}</div>",
        unsafe_allow_html=True,
    )


def render_features() -> None:
    """Render feature summaries for the platform."""
    feature_cols = st.columns(3)
    cards = [
        (
            "Orchestration",
            "Supervisor-led routing",
            "Coordinate classification, escalation, SQL, and knowledge agents from one operator screen.",
        ),
        (
            "Integrations",
            "Salesforce-aware workflows",
            "Keep audio capture and backend workflows close to the CRM and support data plane.",
        ),
        (
            "Operations",
            "Deployment separation",
            "Frontend stays Python-native while backend infra remains isolated under backend/.",
        ),
    ]

    for column, (kicker, title, body) in zip(feature_cols, cards):
        column.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-kicker">{kicker}</div>
                <h3>{title}</h3>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def submit_audio(active_backend_url: str, audio_bytes: bytes) -> None:
    """Send recorded audio to the backend assistant endpoint."""
    files = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}

    try:
        with st.spinner("Sending audio to the assistant..."):
            response = requests.post(active_backend_url, files=files, timeout=60)

        if response.ok:
            data = response.json()
            st.success("Assistant response received.")
            st.markdown(data.get("suggested_response", "No response generated."))
            with st.expander("Raw backend payload"):
                st.json(data)
            return

        st.error(f"Backend returned {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not reach the backend. Start the FastAPI service and retry.")
    except requests.exceptions.Timeout:
        st.error("The backend request timed out. Check the assistant endpoint and try again.")


def render_operator_console(active_backend_url: str) -> None:
    """Render the audio capture and backend submission controls."""
    st.subheader("Operator Console")
    st.caption("Capture audio, inspect the target endpoint, and forward the request to the backend.")

    left_col, right_col = st.columns([1.25, 0.75])

    with left_col:
        audio = audiorecorder("Click to speak", "Recording...")
        if len(audio) > 0:
            audio_bytes = audio.export().read()
            st.audio(audio_bytes)
            if st.button("Send recording", type="primary"):
                submit_audio(active_backend_url, audio_bytes)
        else:
            st.info("Record a question to send voice input to the backend assistant.")

    with right_col:
        st.code(active_backend_url, language="text")
        st.markdown("**Expected request**")
        st.write("Multipart form upload with `audio_file` field.")
        st.markdown("**Current assumptions**")
        st.write("Backend returns JSON with `suggested_response` when the request succeeds.")


def render_debug_tools(active_backend_url: str) -> None:
    """Render a section with debugging tools, like sending a dummy file."""
    with st.expander("Developer & Debugging Tools"):
        st.info(
            "Use these tools to test the backend connection without relying on live components like the audio recorder."
        )
        if st.button("Send Dummy Audio", help="Sends a pre-generated silent WAV file to the backend."):

            def generate_dummy_wav() -> bytes:
                """Generates a minimal, silent 1-second WAV file in memory."""
                # RIFF header
                riff_header = b"RIFF\x24\x08\x00\x00WAVE"
                # fmt chunk
                fmt_chunk = b"fmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00"
                # data chunk
                data_chunk = b"data\x00\x08\x00\x00" + (b"\x00" * 2048)
                return riff_header + fmt_chunk + data_chunk

            dummy_audio_bytes = generate_dummy_wav()
            st.write("Generated a dummy 1-second silent WAV file. Sending to backend...")
            submit_audio(active_backend_url, dummy_audio_bytes)


def main() -> None:
    """Run the Streamlit frontend."""
    render_shell()
    active_backend_url = get_backend_url()

    with st.sidebar:
        st.title("InsightForge")
        st.caption("Streamlit frontend workspace")
        st.write("Use this frontend to validate assistant flows against the FastAPI backend.")
        st.write("Override `INSIGHTFORGE_BACKEND_URL` or Streamlit `BACKEND_URL` secret if needed.")

    render_header(active_backend_url)
    render_features()
    st.divider()
    render_operator_console(active_backend_url)
    render_debug_tools(active_backend_url)


if __name__ == "__main__":
    main()