"""The Escalation Agent: For determining when human intervention is needed."""

from typing import Any
from .base_agent import BaseAgent
from .shared_context import SharedContext


class EscalationAgent(BaseAgent):
    """
    Decides whether a ticket requires human review.

    It analyzes the entire context to look for signs of complexity, high
    customer frustration (sentiment), or a lack of confidence in the generated
    response. If it decides a human is needed, it sets the `escalation_required`
    flag to True and provides a reason.
    """
    @property
    def name(self) -> str:
        return "EscalationAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context