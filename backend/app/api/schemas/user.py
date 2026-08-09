"""Pydantic schemas for User data transfer."""


from pydantic import BaseModel, EmailStr

from app.api.schemas.base import TimeStampedSchema
from app.models.user import RoleEnum


class RoleBase(BaseModel):
    name: RoleEnum
    description: str | None = None


class Role(TimeStampedSchema, RoleBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    role_name: RoleEnum


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None


class User(TimeStampedSchema, UserBase):
    is_active: bool
    role: Role
