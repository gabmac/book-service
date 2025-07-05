from uuid import UUID

from sqlmodel import Field

from .base_model import Base


class BookBookCategoryLink(Base, table=True):
    """Book book categories link model."""

    __tablename__ = "book_book_category_link"  # type: ignore

    book_id: UUID | None = Field(default=None, foreign_key="book.id", primary_key=True)
    book_category_id: UUID | None = Field(
        default=None,
        foreign_key="book_category.id",
        primary_key=True,
    )
