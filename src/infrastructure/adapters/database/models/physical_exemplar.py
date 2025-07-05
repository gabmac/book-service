from typing import List
from uuid import UUID

from sqlmodel import Field, Relationship

from .base_model import Base
from .book_lending import BookLending


class PhysicalExemplar(Base, table=True):
    """Physical book exemplar model."""

    __tablename__ = "physical_exemplar"

    available: bool = Field(nullable=False)
    room: int = Field(nullable=False)
    floor: int = Field(nullable=False)
    bookshelf: int = Field(nullable=False)

    book_id: UUID | None = Field(default=None, foreign_key="book.id")
    book: "Book" = Relationship(back_populates="physical_exemplars")
    branch_id: UUID | None = Field(default=None, foreign_key="branch.id")
    branch: "Branch" = Relationship(back_populates="physical_exemplars")
    lendings: List[BookLending] = Relationship(back_populates="physical_exemplar")
