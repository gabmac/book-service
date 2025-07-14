from datetime import datetime, timezone
from uuid import UUID

from pydantic import Field
from uuid6 import uuid7

from src.domain.entities.base import BaseEntity


class BookCategory(BaseEntity):
    id: UUID = Field(description="Book category id", default_factory=uuid7)
    version: int = Field(description="Book category version", ge=1)
    title: str = Field(description="Book category title")
    description: str | None = Field(
        description="Book category description",
        default=None,
    )
    created_by: str = Field(description="Book category creator")
    updated_by: str = Field(description="Book category updater")
    created_at: datetime = Field(
        description="Book category creation date",
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        description="Book category update date",
        default_factory=lambda: datetime.now(timezone.utc),
    )


class BookCategoryFilter(BaseEntity):
    title: str | None = Field(description="Book category title", default=None)
    description: str | None = Field(
        description="Book category description",
        default=None,
    )
