from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.entities.base import BaseEntity
from src.domain.entities.book import Book
from src.domain.entities.branch import Branch


class PhysicalExemplar(BaseEntity):
    id: UUID = Field(description="Physical exemplar id", default_factory=uuid4)
    available: bool = Field(description="Physical exemplar availability")
    room: int = Field(description="Physical exemplar room", ge=1)
    floor: int = Field(description="Physical exemplar floor", ge=1)
    bookshelf: int = Field(description="Physical exemplar bookshelf", ge=1)
    book_id: UUID = Field(description="Book id")
    book: Book | None = Field(default=None, description="Book")
    branch_id: UUID = Field(description="Branch id")
    branch: Branch | None = Field(default=None, description="Branch")
    created_by: str = Field(description="Physical exemplar creator")
    updated_by: str = Field(description="Physical exemplar updater")
    created_at: datetime = Field(
        description="Physical exemplar creation date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        description="Physical exemplar update date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
