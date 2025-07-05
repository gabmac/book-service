from uuid import UUID
from sqlmodel import Field

from .base import Base


class BookBookCategoriesLink(Base):
    """Book book categories link model."""
    
    book_id: UUID | None = Field(default=None, foreign_key="book.id", primary_key=True)
    book_category_id: UUID | None = Field(default=None, foreign_key="book_category.id", primary_key=True)