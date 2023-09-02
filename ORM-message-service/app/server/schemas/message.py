import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings


class Message_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sender_id: str = Field(...)
    receiver_id: str = Field(...)
    message_type: str = Field(...)
    content: str = Field(...)
    send_date: str = Field(...)
    receive_date: str = Field(...)
    pinned: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sender_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "receiver_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "message_type": "user_message",
                "content": "This is test message",
                "send_date": "2017-10-13T10:53:53Z",
                "receive_date": "2017-10-13T10:53:53Z",
                "pinned": False,
            }
        }

class Update_message_schema(BaseModel):
    sender_id: str = Field(...)
    receiver_id: str = Field(...)
    message_type: str = Field(...)
    content: str = Field(...)
    send_date: str = Field(...)
    receive_date: str = Field(...)
    pinned: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sender_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "receiver_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "message_type": "user_message",
                "content": "This is updated test message",
                "send_date": "2017-10-13T10:53:53Z",
                "receive_date": "2017-10-13T10:53:53Z",
                "pinned": True,
            }
        }

