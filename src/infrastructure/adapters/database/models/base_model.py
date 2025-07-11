from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class Base(SQLModel):
    """Base class for all database models."""

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_by: str = Field(nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_by: str = Field(nullable=False)
