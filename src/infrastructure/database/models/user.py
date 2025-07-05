from enum import Enum
from typing import List
from uuid import UUID
from sqlmodel import Field, Relationship

from infrastructure.database.models.book_lending import BookLending
from infrastructure.database.models.user_configuration import UserConfiguration

from .base import Base


class UserType(Enum):
    """User type enum."""
    
    ADMIN = "admin"
    NORMAL = "normal"
    LIBRARIAN = "librarian"
    STUDENT = "student"
    TEACHER = "teacher"
    
    def __str__(self):
        return self.value

class User(Base):
    """User entity model."""
    
    name: str = Field(nullable=False)
    user_configuration_id: UUID | None = Field(default=None, foreign_key="user_configuration.id")
    active: bool = Field(nullable=False, default=True)
    
    user_configuration: UserConfiguration = Relationship(back_populates="users")
    book_lendings: List[BookLending] = Relationship(back_populates="user")