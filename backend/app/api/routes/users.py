"""API endpoints for managing users."""


from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import User, UserCreate
from app.controllers.user_controller import user_controller
from app.database.session import get_db

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    return await user_controller.create_user(db=db, user_in=user_in)


@router.get("/", response_model=list[User])
async def get_all_users(
    db: AsyncSession = Depends(get_db),  # noqa: B008
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[User]:
    """
    Retrieve all users with pagination.
    """
    return await user_controller.get_all_users(db=db, skip=skip, limit=limit)
