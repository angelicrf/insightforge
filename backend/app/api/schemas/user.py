"""Pydantic schemas for User data transfer."""

from typing import Optional

from pydantic import BaseModel, EmailStr

from app.api.schemas.base import TimeStampedSchema
from app.models.user import RoleEnum


class RoleBase(BaseModel):
    name: RoleEnum
    description: Optional[str] = None


class Role(TimeStampedSchema, RoleBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role_name: RoleEnum


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(TimeStampedSchema, UserBase):
    is_active: bool
    role: Role
