from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic.fields import Field

from src.domain.entities.author import Author
from src.domain.entities.base import BaseEntity
from src.domain.entities.book_category import BookCategory
from src.domain.enums.book_type import BookType


class Book(BaseEntity):
    id: UUID = Field(default_factory=uuid4, description="Book ID")
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
    authors: List[Author] | None = Field(default=None, description="Authors")
    author_ids: List[UUID] | None = Field(default=None, description="Author IDs")
    category_ids: List[UUID] | None = Field(default=None, description="Category IDs")
    book_categories: List[BookCategory] | None = Field(
        default=None,
        description="Book categories",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Book creation date",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Book update date",
    )
    created_by: str = Field(description="Book creator ID")
    updated_by: str = Field(description="Book updater ID")


class BookFilter(BaseEntity):
    isbn_code: Optional[str] = Field(description="Book ISBN code", default=None)
    editor: Optional[str] = Field(description="Book editor", default=None)
    edition: Optional[int] = Field(description="Book edition", default=None)
    type: Optional[BookType] = Field(description="Book type", default=None)
    publish_date: Optional[date] = Field(description="Book publish date", default=None)
    author_name: Optional[str] = Field(description="Author name", default=None)
