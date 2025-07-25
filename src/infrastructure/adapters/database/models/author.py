from typing import List

from sqlmodel import Field, Relationship

from src.infrastructure.adapters.database.models.author_book_link import AuthorBookLink

from .base_model import Base


class Author(Base, table=True):
    """Author entity model."""

    version: int = Field(nullable=False, ge=1)
    name: str = Field(nullable=False, index=True)
    books: List["Book"] = Relationship(  # type: ignore
        back_populates="authors",
        link_model=AuthorBookLink,
    )
