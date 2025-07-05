from uuid import UUID
from sqlmodel import Field, Relationship
from infrastructure.database.models.base import Base


class BookData(Base):
    """Book translation and additional data model."""
    
    language: str = Field(nullable=False)
    summary: str | None = Field(nullable=True)
    title: str = Field(nullable=False)
    
    book_id: UUID | None = Field(default=None, foreign_key="book.id")
    
    book: "Book" = Relationship(back_populates="book_data")