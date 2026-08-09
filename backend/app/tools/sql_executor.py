"""Read-only SQL execution helper."""

import re
from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


def is_read_only_sql(statement: str) -> bool:
    disallowed = re.compile(r"\b(update|delete|drop|insert|alter|truncate)\b", re.IGNORECASE)
    return not bool(disallowed.search(statement))


async def execute_read_only_sql(db: AsyncSession, statement: str) -> List[Dict[str, Any]]:
    if not is_read_only_sql(statement):
        raise ValueError("Only read-only SQL statements are allowed.")

    result = await db.execute(text(statement))
    return [row._asdict() for row in result.mappings().all()]
