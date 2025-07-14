from datetime import datetime, timezone
from uuid import UUID

from pydantic import Field
from uuid6 import uuid7

from src.domain.entities.base import BaseEntity


class Branch(BaseEntity):
    id: UUID = Field(description="Branch id", default_factory=uuid7)
    version: int = Field(description="Branch version", ge=1)
    name: str = Field(description="Branch name")
    created_by: str = Field(description="Branch creator")
    updated_by: str = Field(description="Branch updater")
    created_at: datetime = Field(
        description="Branch creation date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        description="Branch update date",
        default_factory=lambda: datetime.now(timezone.utc),
    )


class BranchFilter(BaseEntity):
    name: str | None = Field(description="Branch name", default=None)
