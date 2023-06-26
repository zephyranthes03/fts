import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Member_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    join_date: str = Field(...)
    post_count: int = Field(...)
    comment_count: int = Field(...)
    point: int = Field(...)
    level: str = Field(...)
    comment: str = Field(...)
    admin_comment: str = Field(...)
    symptom: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "join_date": "2017-10-13T10:53:53Z",
                "post_count": 0,
                "comment_count": 0,
                "point": 0,
                "level": "Normal",
                "comment": "Hello",
                "admin_comment": "Admin Hello",
                "symptom" : "{}"
            }
        }

class Update_member_schema(BaseModel):
    join_date: str = Field(...)
    post_count: int = Field(...)
    comment_count: int = Field(...)
    point: int = Field(...)
    level: str = Field(...)
    comment: str = Field(...)
    admin_comment: str = Field(...)
    symptom: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "join_date": "2017-10-13T10:53:53Z",
                "post_count": 0,
                "comment_count": 0,
                "point": 0,
                "level": "Normal",
                "comment": "Hello",
                "admin_comment": "Admin Hello",
                "symptom" : "{}"
            }
        }

