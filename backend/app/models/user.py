"""SQLAlchemy models for User and Role."""

import enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RoleEnum(str, enum.Enum):
    ADMINISTRATOR = "Administrator"
    SUPPORT_ENGINEER = "Support Engineer"
    MANAGER = "Manager"
    VIEWER = "Viewer"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[RoleEnum] = mapped_column(
        SQLAlchemyEnum(RoleEnum, name="role_name_enum"), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")
