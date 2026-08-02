"""The Supervisor Agent: The central orchestrator of the agentic workflow."""

from typing import Any
from .base_agent import BaseAgent
from .shared_context import SharedContext


class SupervisorAgent(BaseAgent):
    """
    The Supervisor Agent orchestrates the entire ticket resolution process.

    It does not perform tasks itself but instead analyzes the shared context
    and decides which specialized agent to delegate the task to next. It is
    the entry point and the controller of the agentic workflow, ensuring tasks
    are performed in the correct order.
    """
    @property
    def name(self) -> str:
        return "SupervisorAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # In a future phase, this will contain the logic to route the context
        # to other agents based on the state of the context object.
        # For example: if not context.language: route to LanguageAgent
        # if not context.classification: route to ClassificationAgent
        # ...and so on.
        return context