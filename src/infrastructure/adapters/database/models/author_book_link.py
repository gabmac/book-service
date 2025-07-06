from uuid import UUID

from sqlmodel import Field

from .base_model import Base


class AuthorBookLink(Base, table=True):
    """Author book link model."""

    __tablename__ = "author_book_link"  # type: ignore

    author_id: UUID | None = Field(
        default=None,
        foreign_key="author.id",
        primary_key=True,
        index=True,
    )
    book_id: UUID | None = Field(default=None, foreign_key="book.id", primary_key=True)
