from datetime import datetime, timezone
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto, ProcessingResponse
from src.application.dto.book_dto import BookResponse
from src.application.dto.branch import BranchResponse


class PhysicalExemplarCreate(BaseDto):
    available: bool = Field(description="Physical exemplar availability")
    room: int = Field(description="Physical exemplar room", ge=1)
    floor: int = Field(description="Physical exemplar floor", ge=1)
    bookshelf: int = Field(description="Physical exemplar bookshelf", ge=1)
    user: str = Field(description="Physical exemplar user")


class PhysicalExemplarResponse(BaseDto):
    id: UUID = Field(description="Physical exemplar id")
    version: int = Field(description="Version of the data for optimistic locking")
    available: bool = Field(description="Physical exemplar availability")
    room: int = Field(description="Physical exemplar room")
    floor: int = Field(description="Physical exemplar floor")
    bookshelf: int = Field(description="Physical exemplar bookshelf")
    book_id: UUID = Field(description="Book id")
    branch_id: UUID = Field(description="Branch id")
    book: BookResponse = Field(description="Book")
    branch: BranchResponse = Field(description="Branch")
    created_at: datetime = Field(
        description="Physical exemplar creation date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        description="Physical exemplar update date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    created_by: str = Field(description="Physical exemplar creator")
    updated_by: str = Field(description="Physical exemplar updater")


class ProcessingPhysicalExemplar(ProcessingResponse):
    physical_exemplar: PhysicalExemplarResponse = Field(description="Physical exemplar")
