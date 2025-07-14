from typing import List

from sqlmodel import Field, Relationship

from .base_model import Base
from .physical_exemplar import PhysicalExemplar


class Branch(Base, table=True):
    """Library branch entity model."""

    name: str = Field(nullable=False)
    version: int = Field(nullable=False, ge=1)
    physical_exemplars: List[PhysicalExemplar] = Relationship(
        back_populates="branch",
        cascade_delete=True,
    )
