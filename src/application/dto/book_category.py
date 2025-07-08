from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto, ProcessingResponse


class BookCategoryUpsert(BaseDto):
    title: str = Field(description="Book category title")
    description: str | None = Field(
        description="Book category description",
        default=None,
    )
    user: str = Field(description="Book category user")


class BookCategoryResponse(BaseDto):
    id: UUID = Field(description="Book category id")
    title: str = Field(description="Book category title")
    description: str | None = Field(
        description="Book category description",
        default=None,
    )
    created_at: datetime = Field(description="Book category creation date")
    updated_at: datetime = Field(description="Book category update date")
    created_by: str = Field(description="Book category creator")
    updated_by: str = Field(description="Book category updater")


class ProcessingBookCategory(ProcessingResponse):
    book_category: BookCategoryResponse = Field(description="Book category")
