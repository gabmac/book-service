from pydantic import Field
from pydantic.main import BaseModel


class BaseDto(BaseModel):
    class Config:
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        validate_assignment = True
        from_attributes = True


class ProcessingResponse(BaseDto):
    message: str = Field(description="Message", default="Task is processing")
