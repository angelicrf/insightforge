"""Knowledge retrieval helper stub."""

from typing import Any


class KnowledgeSearchTool:
    async def search_documents(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        _ = (query, top_k)
        return []
