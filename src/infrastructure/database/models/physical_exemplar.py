from typing import List
from uuid import UUID
from sqlmodel import Field, Relationship

from infrastructure.database.models.book_lending import BookLending

from .base import Base


class PhysicalExemplar(Base):
    """Physical book exemplar model."""
    
    available: bool = Field(nullable=False)
    room: int = Field(nullable=False)
    floor: int = Field(nullable=False)
    bookshelf: int = Field(nullable=False)
    
    book_id: UUID | None = Field(default=None, foreign_key="book.id")
    book: "Book" = Relationship(back_populates="physical_exemplars")
    branch_id: UUID | None = Field(default=None, foreign_key="branch.id")
    branch: "Branch" = Relationship(back_populates="physical_exemplars")
    lendings: List[BookLending] = Relationship(back_populates="physical_exemplar")