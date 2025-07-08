from pydantic import Field
from pydantic.main import BaseModel


class BaseEntity(BaseModel):
    class Config:
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        validate_assignment = True
        from_attributes = True


class DeletionEntity(BaseEntity):
    id: str = Field(description="Entity id")
