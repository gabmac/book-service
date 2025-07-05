from typing import List
from sqlmodel import Field, Relationship

from infrastructure.database.models.author_book_link import AuthorBookLink

from .base import Base


class Author(Base):
    """Author entity model."""
    
    name: str = Field(nullable=False)
    books: List["Book"] = Relationship(back_populates="authors", link_model=AuthorBookLink)