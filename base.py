"""Base Pydantic schemas for consistent API responses."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BaseSchema(BaseModel):
    """A base schema that enables ORM mode for SQLAlchemy model conversion."""
    model_config = ConfigDict(from_attributes=True)

class TimeStampedSchema(BaseSchema):
    """Schema for models with created_at and updated_at timestamps."""
    id: int
    created_at: datetime
    updated_at: datetime