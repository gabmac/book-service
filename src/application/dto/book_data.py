from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto


class BookDataUpsert(BaseDto):
    summary: str | None = Field(description="Book summary", default=None)
    title: str = Field(description="Book title")
    language: str = Field(description="Book language")


class BookDataResponse(BaseDto):
    id: UUID = Field(description="Book data id")
    summary: str | None = Field(description="Book summary", default=None)
    title: str = Field(description="Book title")
    language: str = Field(description="Book language")
    created_at: datetime = Field(description="Book data creation date")
    updated_at: datetime = Field(description="Book data update date")
    created_by: str = Field(description="Book data creator")
    updated_by: str = Field(description="Book data updater")
