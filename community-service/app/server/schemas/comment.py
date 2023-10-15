import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Comment_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    post_id: str = Field(...)
    comment_re_id: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "post_id": "066de609-b04a-b46c-4b30-32537c7f1f6e",
                "comment_re_id": "",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "like": [],
                "limit" : {},
                "admin_limit" : {}
            }
        }

class Update_comment_schema(BaseModel):
    post_id: str = Field(...)
    comment_id: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "post_id": "066de609-b04a-b46c-4b30-32537c7f1f6e",
                "comment_id": "066de609-4b30-4b30-b04a-32537c7f1f6e",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "like": ["066de609-b04a-4b30-b46c-32537c7f1f6e"],
                "limit" : {"deleted":True},
                "admin_limit" : {"hide":True}
             }
        }


