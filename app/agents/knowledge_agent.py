"""The Knowledge Agent: For retrieving relevant information."""

from typing import Any
from .base_agent import BaseAgent
from .shared_context import SharedContext


class KnowledgeAgent(BaseAgent):
    """
    Retrieves relevant information from the knowledge base (vector database).

    Using the ticket's description and classification from the shared context,
    this agent queries the Qdrant vector store to find the most relevant
    documents, FAQs, or past ticket solutions. It populates the
    `knowledge_snippets` field in the context.
    """
    @property
    def name(self) -> str:
        return "KnowledgeAgent"

    async def run(self, context: SharedContext) -> SharedContext:
        # Implementation will go here in a future phase.
        return context