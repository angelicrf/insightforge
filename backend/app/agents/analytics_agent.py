"""The Analytics Agent: For interpreting metrics and logs."""

from typing import Any

from .base_agent import BaseAgent
from .shared_context import SharedContext


class AnalyticsAgent(BaseAgent):
    """
    Interprets data and generates natural language summaries about metrics.

    This agent can take results from a SQL query (e.g., from `ai_logs`) and
    create a human-readable explanation or summary, which can be used in
    reports or dashboards.
    """
    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)

    @property
    def name(self) -> str:
        return "AnalyticsAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context