from enum import StrEnum
from sqlmodel import Field, Relationship

from .base import Base
from typing import List

class UserType(StrEnum):
    """User type enum."""
    
    ADMIN = "admin"
    NORMAL = "normal"
    LIBRARIAN = "librarian"
    STUDENT = "student"
    TEACHER = "teacher"


class UserConfiguration(Base):
    """User configuration model."""
    
    user_type: UserType = Field(nullable=False)
    max_books: int = Field(nullable=False)
    
    users: List["User"] = Relationship(back_populates="user_configuration")