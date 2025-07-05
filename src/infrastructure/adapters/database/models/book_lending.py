from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship

from .base_model import Base


class BookLending(Base, table=True):
    """Book lending transaction model."""

    __tablename__ = "book_lending"

    reserved_at: datetime | None = Field(nullable=True)
    lend_at: datetime | None = Field(nullable=True)
    returned_at: datetime | None = Field(nullable=True)
    planned_returned_at: datetime | None = Field(nullable=True)

    physical_exemplar_id: UUID | None = Field(
        default=None,
        foreign_key="physical_exemplar.id",
    )
    physical_exemplar: "PhysicalExemplar" = Relationship(back_populates="lendings")
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="book_lendings")
