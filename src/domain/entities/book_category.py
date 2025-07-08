from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.entities.base import BaseEntity


class BookCategory(BaseEntity):
    id: UUID = Field(description="Book category id", default_factory=uuid4)
    title: str = Field(description="Book category title")
    description: str | None = Field(
        description="Book category description",
        default=None,
    )
    created_by: str = Field(description="Book category creator")
    updated_by: str = Field(description="Book category updater")
    created_at: datetime = Field(
        description="Book category creation date",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Book category update date",
        default_factory=datetime.now,
    )
