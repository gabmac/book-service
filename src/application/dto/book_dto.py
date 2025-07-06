from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field

from src.domain.enums.book_type import BookType


class Book(BaseModel):
    isbn_code: str = Field(description="Book ISBN code")
    editor: str = Field(description="Book editor")
    edition: int = Field(description="Book edition")
    type: BookType = Field(description="Book type")
    publish_date: datetime = Field(description="Book publish date")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Book creation date",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Book update date",
    )
    created_by: str = Field(description="Book creator ID")
    updated_by: str = Field(description="Book updater ID")
