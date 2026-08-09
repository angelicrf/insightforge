"""
API routes for inspecting the Neon database.
"""

import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import RoleEnum
from app.security.dependencies import require_roles

router = APIRouter(
    dependencies=[Depends(require_roles([RoleEnum.ADMINISTRATOR]))]
)


@router.get("/tables")
async def get_all_tables(db: AsyncSession = Depends(get_db)) -> dict:
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
async def get_table_data(table_name: str, db: AsyncSession = Depends(get_db)) -> dict:
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

    # This is still a raw SQL query and should be used with caution.
    # The table name is validated, but this pattern is generally discouraged.
    query = f"SELECT * FROM {table_name}"
    result = await db.execute(text(query))
    return {"rows": [dict(row) for row in result.mappings().all()]}
