from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.entities.base import BaseEntity


class Branch(BaseEntity):
    id: UUID = Field(description="Branch id", default_factory=uuid4)
    name: str = Field(description="Branch name")
    created_by: str = Field(description="Branch creator")
    updated_by: str = Field(description="Branch updater")
    created_at: datetime = Field(
        description="Branch creation date",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Branch update date",
        default_factory=datetime.now,
    )


class BranchFilter(BaseEntity):
    name: str | None = Field(description="Branch name", default=None)
