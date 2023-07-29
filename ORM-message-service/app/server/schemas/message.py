import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Message_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sender_id: str = Field(...)
    receiver_id: str = Field(...)
    content: str = Field(...)
    send_date: str = Field(...)
    check_date: str = Field(...)
    read_flag: bool = Field(...)
    conversation_id: str = Field(...)
    message_type: str = Field(...)
    community_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sender_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "receiver_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "content": "This is test message",
                "send_date": "2017-10-13T10:53:53Z",
                "check_date": "2017-10-13T10:53:53Z",
                "read_flag": False,
                "conversation_id": "",
                "message_type": "user",
                "community_id": ""
            }
        }

class Update_message_schema(BaseModel):
    sender_id: str = Field(...)
    receiver_id: str = Field(...)
    content: str = Field(...)
    send_date: str = Field(...)
    check_date: str = Field(...)
    read_flag: bool = Field(...)
    conversation_id: str = Field(...)
    message_type: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sender_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "receiver_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "content": "This is test message",
                "send_date": "2017-10-13T10:53:53Z",
                "check_date": "2017-10-13T10:53:53Z",
                "read_flag": False,
                "conversation_id": "",
                "message_type": "user",
                "community_id": ""
            }
        }

