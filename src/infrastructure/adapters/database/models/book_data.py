from uuid import UUID

from sqlmodel import Field, Relationship

from .base_model import Base


class BookData(Base, table=True):
    """Book translation and additional data model."""

    __tablename__ = "book_data"  # type: ignore

    language: str = Field(nullable=False)
    summary: str | None = Field(nullable=True)
    title: str = Field(nullable=False, index=True)

    book_id: UUID | None = Field(default=None, foreign_key="book.id")

    book: "Book" = Relationship(  # type: ignore
        back_populates="book_data",
    )
