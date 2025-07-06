from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto


class AuthorCreate(BaseDto):
    name: str = Field(description="Author name")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Book creation date",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Book update date",
    )
    user: str = Field(description="Author user")


class AuthorFilter(BaseDto):
    name: Optional[str] = Field(description="Author name", default=None)


class AuthorResponse(BaseDto):
    id: UUID = Field(description="Author ID")
    name: str = Field(description="Author name")
    created_at: datetime = Field(description="Author creation date")
    updated_at: datetime = Field(description="Author update date")
    created_by: str = Field(description="Author creator")
    updated_by: str = Field(description="Author updater")
