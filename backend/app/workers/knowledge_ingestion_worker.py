"""Knowledge ingestion worker stub."""

from typing import Any


async def process_document(ctx: dict[str, Any], document_id: int) -> dict[str, Any]:
    _ = ctx
    return {"document_id": document_id, "status": "processed"}
