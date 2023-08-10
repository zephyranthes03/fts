import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Post_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    related_post_id: str = Field(...)
    re_id: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    update_date: str = Field(...)
    pinned: bool = Field(...)
    read_count: int = Field(...)
    like_count: int = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)
    tag: list = Field(...)


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "related_post_id": "test",
                "re_id": "",
                "title": "title",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "update_date": "2017-10-13T10:53:53Z",
                "pinned": True,
                "read_count": 0,
                "like_count": 0,
                "like": [],
                "limit" : {},
                "admin_limit" : {},
                "tag": ['tag1', 'tag2']
            }
        }

class Update_post_schema(BaseModel):
    related_post_id: str = Field(...)
    re_id: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    update_date: str = Field(...)
    pinned: bool = Field(...)
    read_count: int = Field(...)
    like_count: int = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)
    tag: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "related_post_id": "test",
                "re_id": "",
                "title": "title",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "update_date": "2017-10-13T10:53:53Z",
                "pinned": True,
                "read_count": 1,
                "like_count": 1,
                "like": ["066de609-b04a-4b30-b46c-32537c7f1f6e"],
                "limit" : {"deleted":True},
                "admin_limit" : {"hide":True},
                "tag": ['tag1', 'tag2','tag3']
            }
        }


