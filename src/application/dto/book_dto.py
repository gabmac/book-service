from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic.fields import Field

from src.application.dto.base import BaseDto
from src.domain.enums.book_type import BookType


class Book(BaseDto):
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
    user: str = Field(description="Book user")


class BookFilter(BaseDto):
    isbn_code: Optional[str] = Field(description="Book ISBN code", default=None)
    editor: Optional[str] = Field(description="Book editor", default=None)
    edition: Optional[int] = Field(description="Book edition", default=None)
    type: Optional[BookType] = Field(description="Book type", default=None)
    publish_date: Optional[date] = Field(description="Book publish date", default=None)


class BookResponse(BaseDto):
    id: UUID = Field(description="Book ID")
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
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
