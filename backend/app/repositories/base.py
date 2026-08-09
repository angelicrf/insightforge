"""Base repository primitive used by concrete repositories."""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic repository that stores the SQLAlchemy model type."""

    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelT | None:
        """Retrieve a single object by its primary key."""
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelT]:
        """Retrieve multiple objects with pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())
