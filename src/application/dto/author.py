from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto, ProcessingResponse


class AuthorUpsert(BaseDto):
    name: str = Field(description="Author name")
    user: str = Field(description="Author user")


class AuthorFilter(BaseDto):
    name: Optional[str] = Field(description="Author name", default=None)


class AuthorResponse(BaseDto):
    id: UUID = Field(description="Author ID")
    version: int = Field(description="Author version")
    name: str = Field(description="Author name")
    created_at: datetime = Field(description="Author creation date")
    updated_at: datetime = Field(description="Author update date")
    created_by: str = Field(description="Author creator")
    updated_by: str = Field(description="Author updater")


class ProcessingAuthor(ProcessingResponse):
    author: AuthorResponse = Field(description="Author")
