"""The Language Agent: For detecting the language of a ticket."""

from typing import Any

from .base_agent import BaseAgent
from .shared_context import SharedContext


class LanguageAgent(BaseAgent):
    """
    Specializes in detecting the primary language of the ticket's content.

    It reads the ticket description and writes its finding (e.g., 'en', 'es')
    into the `language` field of the shared context.
    """
    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)

    @property
    def name(self) -> str:
        return "LanguageAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context