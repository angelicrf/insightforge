"""Public table-inspection routes kept for backwards compatibility."""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

router = APIRouter()


@router.get("/tables")
async def get_all_tables(db: AsyncSession = Depends(get_db)) -> dict:
    """Return all table names in the public schema."""
    if not db:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database session not available.")

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
    return {"tables": [row[0] for row in result.fetchall()]}


@router.get("/tables/{table_name}")
async def get_table_data(table_name: str, db: AsyncSession = Depends(get_db)) -> dict:
    """Return all rows for one public table after strict name validation."""
    if not re.match(r"^[a-zA-Z0-9_]+$", table_name):
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

    query = f"SELECT * FROM {table_name}"
    result = await db.execute(text(query))
    return {"rows": [dict(row) for row in result.mappings().all()]}
