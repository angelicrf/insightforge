"""Repository for Role model."""


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Role, RoleEnum
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for all Role model related database operations."""

    def __init__(self) -> None:
        super().__init__(Role)

    async def get_by_name(self, db: AsyncSession, *, name: RoleEnum) -> Role | None:
        """Retrieve a role by its enum name."""
        statement = select(self.model).where(self.model.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()


role_repository = RoleRepository()