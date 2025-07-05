from datetime import datetime
from enum import StrEnum
from typing import List
from sqlmodel import Field, Relationship

from infrastructure.database.models.author import Author
from infrastructure.database.models.author_book_link import AuthorBookLink
from infrastructure.database.models.book_book_category_link import BookBookCategoriesLink
from infrastructure.database.models.book_category import BookCategory
from infrastructure.database.models.book_data import BookData
from infrastructure.database.models.physical_exemplar import PhysicalExemplar

from .base import Base

class BookType(StrEnum):
    """Book type enum."""
    
    PHYSICAL = "physical"
    EBOOK = "ebook"

class Book(Base):
    """Book entity model."""
    
    isbn_code: str = Field(nullable=False, unique=True)
    editor: str = Field(nullable=False)
    edition: int = Field(nullable=False)
    type: BookType = Field(nullable=False)
    publish_date: datetime = Field(nullable=False)
    
    authors: List[Author] = Relationship(back_populates="books", link_model=AuthorBookLink)
    book_categories: List[BookCategory] = Relationship(back_populates="books", link_model=BookBookCategoriesLink)
    book_data: List[BookData] = Relationship(back_populates="book", cascade_delete=True)
    physical_exemplars: List[PhysicalExemplar] = Relationship(back_populates="book", cascade_delete=True)