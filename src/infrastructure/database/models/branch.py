from typing import List
from sqlmodel import Field, Relationship

from infrastructure.database.models.physical_exemplar import PhysicalExemplar

from .base import Base


class Branch(Base):
    """Library branch entity model."""
    
    name: str = Field(nullable=False)
    physical_exemplars: List[PhysicalExemplar] = Relationship(back_populates="branch", cascade_delete=True)