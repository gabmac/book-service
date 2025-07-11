from datetime import datetime, timezone
from uuid import UUID

from pydantic import Field
from uuid6 import uuid7

from src.domain.entities.base import BaseEntity


class BookData(BaseEntity):
    id: UUID = Field(description="Book data id", default_factory=uuid7)
    summary: str | None = Field(description="Book summary", default=None)
    title: str = Field(description="Book title")
    language: str = Field(description="Book language")
    created_at: datetime = Field(
        description="Book data creation date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        description="Book data update date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    created_by: str = Field(description="Book data creator")
    updated_by: str = Field(description="Book data updater")
