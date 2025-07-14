from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.application.dto.base import BaseDto, ProcessingResponse


class BranchResponse(BaseDto):
    id: UUID = Field(description="Branch id")
    version: int = Field(description="Branch version")
    name: str = Field(description="Branch name")
    created_at: datetime = Field(
        description="Branch creation date",
    )
    updated_at: datetime = Field(
        description="Branch update date",
    )
    created_by: str = Field(description="Branch creator")
    updated_by: str = Field(description="Branch updater")


class ProcessingBranch(ProcessingResponse):
    branch: BranchResponse = Field(description="Branch")


class BranchFilter(BaseDto):
    name: str | None = Field(description="Branch name", default=None)


class BranchUpsert(BaseDto):
    name: str = Field(description="Branch name")
    user: str = Field(description="Branch user")
