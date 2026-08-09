"""Service layer for user-related business logic."""


from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate
from app.models.user import User
from app.repositories.role_repository import role_repository
from app.repositories.user_repository import user_repository
from app.security import password as password_service


class UserService:
    """
    Encapsulates business logic for user management and authentication.
    """

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Creates a new user, ensuring email is not already taken.
        """
        # Check if a user with this email already exists
        existing_user = await user_repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        # Hash the password before storing
        hashed_password = password_service.get_password_hash(user_in.password)

        # Fetch the role from the database
        role = await role_repository.get_by_name(db, name=user_in.role_name)
        if not role:
            # This case should ideally not happen if roles are pre-seeded
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role '{user_in.role_name}' does not exist.",
            )

        # Create user object (excluding password and role_name from the direct model creation)
        user_data = user_in.model_dump(exclude={"password", "role_name"})
        db_user = User(**user_data, hashed_password=hashed_password, role_id=role.id)

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> User | None:
        """
        Authenticates a user by email and password.
        """
        user = await user_repository.get_by_email(db, email=email)
        if not user or not password_service.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_all_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Retrieves a list of users with pagination.
        """
        return await user_repository.get_multi(db=db, skip=skip, limit=limit)


user_service = UserService()