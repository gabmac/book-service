from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Base(SQLModel, table=True):
    """Base class for all database models."""
    
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    created_by: str = Field(nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_by: str = Field(nullable=False)