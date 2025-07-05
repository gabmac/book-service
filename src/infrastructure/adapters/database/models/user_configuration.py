from typing import List

from sqlmodel import Field, Relationship

from src.domain.enums.user_type import UserType

from .base_model import Base


class UserConfiguration(Base, table=True):
    """User configuration model."""

    __tablename__ = "user_configuration"  # type: ignore

    user_type: UserType = Field(nullable=False)
    max_books: int = Field(nullable=False)

    users: List["User"] = Relationship(  # type: ignore
        back_populates="user_configuration",
    )
