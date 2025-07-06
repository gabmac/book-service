from datetime import date
from typing import List

from sqlmodel import Field, Relationship

from src.domain.enums.book_type import BookType

from .author import Author
from .author_book_link import AuthorBookLink
from .base_model import Base
from .book_book_category_link import BookBookCategoryLink
from .book_category import BookCategory
from .book_data import BookData
from .physical_exemplar import PhysicalExemplar


class Book(Base, table=True):
    """Book entity model."""

    isbn_code: str = Field(nullable=False, unique=True)
    editor: str = Field(nullable=False)
    edition: int = Field(nullable=False)
    type: BookType = Field(nullable=False)
    publish_date: date = Field(nullable=False)

    authors: List[Author] = Relationship(
        back_populates="books",
        link_model=AuthorBookLink,
    )
    book_categories: List[BookCategory] = Relationship(
        back_populates="books",
        link_model=BookBookCategoryLink,
    )
    book_data: List[BookData] = Relationship(back_populates="book", cascade_delete=True)
    physical_exemplars: List[PhysicalExemplar] = Relationship(
        back_populates="book",
        cascade_delete=True,
    )
