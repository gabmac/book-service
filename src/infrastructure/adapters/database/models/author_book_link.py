from uuid import UUID

from sqlmodel import Field

from .base_model import Base


class AuthorBookLink(Base, table=True):
    """Author book link model."""

    __tablename__ = "author_book_link"  # type: ignore

    author_id: UUID = Field(
        foreign_key="author.id",
        index=True,
        default=None,
    )
    book_id: UUID = Field(
        default=None,
        foreign_key="book.id",
        index=True,
        ondelete="CASCADE",
    )
