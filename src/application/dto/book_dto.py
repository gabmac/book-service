from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic.fields import Field

from src.application.dto.author import AuthorResponse
from src.application.dto.base import BaseDto, ProcessingResponse
from src.application.dto.book_category import BookCategoryResponse
from src.application.dto.book_data import BookDataResponse, BookDataUpsert
from src.domain.enums.book_type import BookType


class Book(BaseDto):
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition", ge=1)
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
    book_data: List[BookDataUpsert] = Field(
        default_factory=list,
        description="Book data",
    )
    author_ids: Optional[List[UUID]] = Field(
        default=None,
        description="Author IDs",
        min_length=1,
    )
    category_ids: Optional[List[UUID]] = Field(
        default=None,
        description="Category IDs",
    )
    user: str = Field(description="Book user")


class BookFilter(BaseDto):
    isbn_code: Optional[str] = Field(description="Book ISBN code", default=None)
    editor: Optional[str] = Field(description="Book editor", default=None)
    edition: Optional[int] = Field(description="Book edition", default=None)
    type: Optional[BookType] = Field(description="Book type", default=None)
    author_name: Optional[str] = Field(description="Author name", default=None)
    publish_date: Optional[date] = Field(description="Book publish date", default=None)
    book_category_name: Optional[str] = Field(
        description="Book category name",
        default=None,
    )


class BookResponse(BaseDto):
    id: UUID = Field(description="Book ID")
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: date = Field(description="Book publish date")
    authors: List[AuthorResponse] | None = Field(
        default=None,
        description="Book authors",
    )
    book_categories: List[BookCategoryResponse] | None = Field(
        default=None,
        description="Book categories",
    )
    book_data: List[BookDataResponse] | None = Field(
        default=None,
        description="Book data",
    )


class ProcessingBook(ProcessingResponse):
    book: BookResponse = Field(description="Book")
