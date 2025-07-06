from pydantic import Field

from src.application.dto.base import BaseDto


class Message(BaseDto):
    queue_name: str = Field(description="Queue name")
    message: str = Field(description="Message")
