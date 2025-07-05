from typing import List
from sqlmodel import Field, Relationship

from infrastructure.database.models.book_book_category_link import BookBookCategoriesLink

from .base import Base


class BookCategory(Base):
    """Book category model."""
    
    name: str = Field(nullable=False)
    description: str | None = Field(nullable=True)
    books: List["Book"] = Relationship(back_populates="book_categories", link_model=BookBookCategoriesLink)
    