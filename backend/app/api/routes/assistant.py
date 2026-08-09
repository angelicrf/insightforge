"""Assistant endpoints used by the Streamlit frontend."""

from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

router = APIRouter()


@router.post("/query")
async def assistant_query(
    audio_file: UploadFile = File(..., description="Recorded operator audio as WAV/MP3."),
    user_query_text: str | None = Form(default=None),
) -> dict:
    """Accept operator audio and return a frontend-compatible assistant response."""
    audio_bytes = await audio_file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="audio_file is empty.")

    # Keep response schema aligned with frontend expectations while backend workflows evolve.
    response_text = (
        f"Received {len(audio_bytes)} bytes from '{audio_file.filename or 'audio upload'}'. "
        "Assistant workflow endpoint is reachable."
    )
    if user_query_text:
        response_text = f"{response_text} Query text: {user_query_text}"

    return {
        "suggested_response": response_text,
        "audio_filename": audio_file.filename,
        "content_type": audio_file.content_type,
        "bytes_received": len(audio_bytes),
    }
