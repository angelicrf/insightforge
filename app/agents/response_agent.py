"""The Response Agent: For drafting communications to the customer."""

from typing import Any
from .base_agent import BaseAgent
from .shared_context import SharedContext


class ResponseAgent(BaseAgent):
    """
    Generates a draft response to the customer.

    This agent synthesizes all information available in the shared context—the
    original ticket, customer details, classification, and retrieved knowledge
    snippets—to compose a helpful, empathetic, and accurate response. The
    draft is placed in the `suggested_response` field of the context.
    """
    @property
    def name(self) -> str:
        return "ResponseAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context