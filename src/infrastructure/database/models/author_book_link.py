from uuid import UUID
from sqlmodel import Field

from .base import Base


class AuthorBookLink(Base):
    """Author book link model."""
    
    author_id: UUID | None = Field(default=None, foreign_key="author.id", primary_key=True)
    book_id: UUID | None = Field(default=None, foreign_key="book.id", primary_key=True)