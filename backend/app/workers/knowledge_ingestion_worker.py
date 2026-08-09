"""Knowledge ingestion worker stub."""

from typing import Any, Dict


async def process_document(ctx: Dict[str, Any], document_id: int) -> Dict[str, Any]:
    _ = ctx
    return {"document_id": document_id, "status": "processed"}
