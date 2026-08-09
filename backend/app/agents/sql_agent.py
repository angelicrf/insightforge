"""The SQL Agent: For generating read-only SQL queries."""

from typing import Any

from .base_agent import BaseAgent
from .shared_context import SharedContext


class SQLAgent(BaseAgent):
    """
    Generates a read-only SQL query from a natural language question.

    It takes a user's question from the context, constructs a prompt with
    schema information, and asks the LLM to generate a SQL query. The query
    is then placed in the `generated_sql_query` field. This agent does NOT
    execute the query; it only generates it.
    """
    def __init__(self, llm_provider: Any):
        super().__init__(llm_provider)

    @property
    def name(self) -> str:
        return "SQLAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context