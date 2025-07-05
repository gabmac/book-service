from typing import List

from sqlmodel import Field, Relationship

from src.infrastructure.adapters.database.models.author_book_link import AuthorBookLink

from .base_model import Base


class Author(Base, table=True):
    """Author entity model."""

    name: str = Field(nullable=False)
    books: List["Book"] = Relationship(  # type: ignore
        back_populates="authors",
        link_model=AuthorBookLink,
    )
