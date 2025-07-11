from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlmodel import Field
from uuid6 import uuid7

from src.domain.entities.base import BaseEntity


class Author(BaseEntity):
    """Author entity model."""

    id: UUID = Field(description="Author ID", default_factory=uuid7)
    name: str = Field(description="Author name")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Book creation date",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Book update date",
    )
    created_by: str = Field(description="Book creator ID")
    updated_by: str = Field(description="Book updater ID")


class AuthorFilter(BaseEntity):
    name: Optional[str] = Field(description="Author name")
