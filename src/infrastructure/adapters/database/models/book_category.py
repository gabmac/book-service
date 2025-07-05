from typing import List

from sqlmodel import Field, Relationship

from .base_model import Base
from .book_book_category_link import BookBookCategoryLink


class BookCategory(Base, table=True):
    """Book category model."""

    __tablename__ = "book_category"

    name: str = Field(nullable=False)
    description: str | None = Field(nullable=True)
    books: List["Book"] = Relationship(
        back_populates="book_categories",
        link_model=BookBookCategoryLink,
    )
