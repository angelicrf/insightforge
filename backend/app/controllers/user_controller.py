"""Controller for user-related API operations."""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.schemas.user import UserCreate
from app.services.user_service import user_service
from app.models.user import User


class UserController:
    """Orchestrates user-related operations by calling the user service."""

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Handles the business logic of creating a user via the user service."""
        return await user_service.create_user(db=db, user_in=user_in)

    async def get_all_users(self, db: AsyncSession, skip: int, limit: int) -> List[User]:
        """Handles the business logic of retrieving all users via the user service."""
        return await user_service.get_all_users(db=db, skip=skip, limit=limit)


user_controller = UserController()