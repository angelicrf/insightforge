"""
API routes for inspecting the Neon database.
"""

import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import MetaData, Table, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import RoleEnum
from app.security.dependencies import require_roles

router = APIRouter(
    dependencies=[Depends(require_roles([RoleEnum.ADMINISTRATOR]))]
)


async def _fetch_table_rows(db: AsyncSession, table_name: str) -> list[dict]:
    """Fetch all rows from a validated public table using reflected metadata."""
    query = await db.run_sync(
        lambda sync_session: select(
            Table(table_name, MetaData(), autoload_with=sync_session.connection())
        )
    )
    result = await db.execute(query)
    return [dict(row) for row in result.mappings().all()]


@router.get("/tables")
async def get_all_tables(db: AsyncSession = Depends(get_db)) -> dict:  # noqa: B008
    """Fetches a list of all table names in the public schema."""
    if db:
        result = await db.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
        )
        tables = [row[0] for row in result.fetchall()]
        return {"tables": tables or []}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database session not available.")


@router.get("/tables/{table_name}")
async def get_table_data(table_name: str, db: AsyncSession = Depends(get_db)) -> dict:  # noqa: B008
    """Fetches all rows from a specific table and returns them as dictionaries."""
    # Strict validation to prevent SQL injection since table names can't be parameterized
    if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name format.")

    table_exists_result = await db.execute(
        text(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = :table_name
            LIMIT 1
            """
        ),
        {"table_name": table_name},
    )
    if table_exists_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Table '{table_name}' not found.")

    return {"rows": await _fetch_table_rows(db, table_name)}
