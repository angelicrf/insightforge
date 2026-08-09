"""Knowledge retrieval helper stub."""

from typing import Any, Dict, List


class KnowledgeSearchTool:
    async def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        _ = (query, top_k)
        return []
