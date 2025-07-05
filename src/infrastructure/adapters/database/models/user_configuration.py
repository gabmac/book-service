from enum import StrEnum
from typing import List

from sqlmodel import Field, Relationship

from .base_model import Base


class UserType(StrEnum):
    """User type enum."""

    ADMIN = "admin"
    NORMAL = "normal"
    LIBRARIAN = "librarian"
    STUDENT = "student"
    TEACHER = "teacher"


class UserConfiguration(Base, table=True):
    """User configuration model."""

    __tablename__ = "user_configuration"

    user_type: UserType = Field(nullable=False)
    max_books: int = Field(nullable=False)

    users: List["User"] = Relationship(back_populates="user_configuration")
