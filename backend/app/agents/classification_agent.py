"""The Classification Agent: For understanding and categorizing tickets."""

from typing import Any

from .base_agent import BaseAgent
from .shared_context import SharedContext


class ClassificationAgent(BaseAgent):
    """
    Specializes in analyzing a support ticket's content to classify it.

    Its primary tasks are to determine the ticket's category (e.g., "Billing",
    "Technical Issue"), priority, and sentiment. It reads the ticket
    description from the context and writes its findings back into the
    `classification` field of the context.
    """
    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)

    @property
    def name(self) -> str:
        return "ClassificationAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context