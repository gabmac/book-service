from datetime import date, datetime, timezone
from typing import List, Optional
from uuid import UUID

from pydantic.fields import Field
from uuid6 import uuid7

from src.domain.entities.author import Author
from src.domain.entities.base import BaseEntity
from src.domain.entities.book_category import BookCategory
from src.domain.entities.book_data import BookData
from src.domain.enums.book_type import BookType


class Book(BaseEntity):
    id: UUID = Field(default_factory=uuid7, description="Book ID")
    version: int = Field(description="Version of the data for optimistic locking", ge=1)
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
    authors: List[Author] | None = Field(default=None, description="Authors")
    author_ids: List[UUID] | None = Field(default=None, description="Author IDs")
    category_ids: List[UUID] | None = Field(default=None, description="Category IDs")
    book_data: List[BookData] | None = Field(default=None, description="Book data")
    book_categories: List[BookCategory] | None = Field(
        default=None,
        description="Book categories",
    )
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


class BookSearchFilter(BaseEntity):
    """Enhanced search filter for Elasticsearch book queries"""

    # Basic book fields
    isbn_code: Optional[str] = Field(description="Book ISBN code", default=None)
    editor: Optional[str] = Field(description="Book editor", default=None)
    edition: Optional[int] = Field(description="Book edition", default=None)
    type: Optional[BookType] = Field(description="Book type", default=None)
    publish_date_from: Optional[date] = Field(
        description="Publish date from",
        default=None,
    )
    publish_date_to: Optional[date] = Field(description="Publish date to", default=None)

    # Full-text search
    text_query: Optional[str] = Field(
        description="Full-text search query",
        default=None,
    )
    title_query: Optional[str] = Field(
        description="Search in book titles",
        default=None,
    )
    summary_query: Optional[str] = Field(
        description="Search in book summaries",
        default=None,
    )

    # Author filters
    author_name: Optional[str] = Field(description="Author name", default=None)

    # Category filters
    category_title: Optional[str] = Field(description="Category title", default=None)

    # Language filters
    languages: Optional[List[str]] = Field(description="Book languages", default=None)

    # Pagination
    page: int = Field(description="Page number", default=1)
    size: int = Field(description="Page size", default=10)

    # Sorting
    sort_by: Optional[str] = Field(description="Sort field", default="created_at")
    sort_order: Optional[str] = Field(
        description="Sort order (asc/desc)",
        default="desc",
    )

    # Advanced options
    fuzzy_search: bool = Field(description="Enable fuzzy matching", default=False)
    highlight_fields: Optional[List[str]] = Field(
        description="Fields to highlight",
        default=None,
    )

    _basic_filters = {"edition", "type"}
