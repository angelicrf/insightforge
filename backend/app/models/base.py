"""Base class for all SQLAlchemy models."""

from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

timestamp_tz = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP")),
]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[timestamp_tz]
    updated_at: Mapped[timestamp_tz] = mapped_column(onupdate=datetime.utcnow)
