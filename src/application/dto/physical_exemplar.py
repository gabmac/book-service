from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto, ProcessingResponse


class PhysicalExemplarCreate(BaseDto):
    available: bool = Field(description="Physical exemplar availability")
    room: int = Field(description="Physical exemplar room", ge=1)
    floor: int = Field(description="Physical exemplar floor", ge=1)
    bookshelf: int = Field(description="Physical exemplar bookshelf", ge=1)
    user: str = Field(description="Physical exemplar user")


class PhysicalExemplarResponse(BaseDto):
    id: UUID = Field(description="Physical exemplar id")
    available: bool = Field(description="Physical exemplar availability")
    room: int = Field(description="Physical exemplar room")
    floor: int = Field(description="Physical exemplar floor")
    bookshelf: int = Field(description="Physical exemplar bookshelf")
    book_id: UUID = Field(description="Book id")
    branch_id: UUID = Field(description="Branch id")
    created_at: datetime = Field(
        description="Physical exemplar creation date",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Physical exemplar update date",
        default_factory=datetime.now,
    )
    created_by: str = Field(description="Physical exemplar creator")
    updated_by: str = Field(description="Physical exemplar updater")


class ProcessingPhysicalExemplar(ProcessingResponse):
    physical_exemplar: PhysicalExemplarResponse = Field(description="Physical exemplar")
