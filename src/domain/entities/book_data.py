from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.entities.base import BaseEntity


class BookData(BaseEntity):
    id: UUID = Field(description="Book data id", default_factory=uuid4)
    summary: str | None = Field(description="Book summary", default=None)
    title: str = Field(description="Book title")
    language: str = Field(description="Book language")
    created_at: datetime = Field(
        description="Book data creation date",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Book data update date",
        default_factory=datetime.now,
    )
    created_by: str = Field(description="Book data creator")
    updated_by: str = Field(description="Book data updater")
