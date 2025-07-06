from uuid import UUID

from sqlmodel import Field, Relationship

from .base_model import Base


class PhysicalExemplar(Base, table=True):
    """Physical book exemplar model."""

    __tablename__ = "physical_exemplar"  # type: ignore

    available: bool = Field(nullable=False)
    room: int = Field(nullable=False)
    floor: int = Field(nullable=False)
    bookshelf: int = Field(nullable=False)

    book_id: UUID | None = Field(default=None, foreign_key="book.id", index=True)
    book: "Book" = Relationship(  # type: ignore
        back_populates="physical_exemplars",
    )
    branch_id: UUID | None = Field(default=None, foreign_key="branch.id", index=True)
    branch: "Branch" = Relationship(  # type: ignore
        back_populates="physical_exemplars",
    )
