"""Agent for converting voice audio to text."""

import io
from typing import Any

import httpx
import structlog
from openai import AsyncOpenAI

from app.config.settings import settings

from .base_agent import BaseAgent
from .shared_context import SharedContext

log = structlog.get_logger()


class VoiceToTextAgent(BaseAgent):
    """An agent that converts audio data into transcribed text."""

    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
            log.warning("OPENAI_API_KEY not found. VoiceToTextAgent will not be able to transcribe audio.")

    @property
    def name(self) -> str:
        return "VoiceToTextAgent"

    async def _transcribe_audio_with_whisper(self, audio_data: bytes) -> str:
        """
        Uses the OpenAI Whisper API to transcribe audio data.
        """
        if not self.client:
            log.error("OpenAI client not initialized. Cannot transcribe audio.")
            return "Error: Transcription service not configured."

        log.info("Transcribing audio with OpenAI Whisper...")
        try:
            # The API expects a file-like object, so we wrap the bytes in BytesIO.
            # We also need to provide a file name, e.g., "audio.wav".
            audio_file = ("audio.wav", io.BytesIO(audio_data), "audio/wav")

            response = await self.client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
            return response.text
        except httpx.HTTPStatusError as e:
            log.error("Error calling Whisper API", error=e, response_text=e.response.text)
            return f"Error: Failed to transcribe audio. Status: {e.response.status_code}"

    async def run(self, context: SharedContext) -> SharedContext:
        """Transcribes audio from the context and updates it with the text."""
        if context.user_query_audio and not context.user_query_text:
            log.info("Transcribing user audio query...")
            transcribed_text = await self._transcribe_audio_with_whisper(context.user_query_audio)
            context.user_query_text = transcribed_text
            log.info("Transcription complete.", transcribed_text=transcribed_text)
        return context