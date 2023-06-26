import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Board_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    update_date: str = Field(...)
    pinned: bool = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "title",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "update_date": "2017-10-13T10:53:53Z",
                "pinned": True,
                "like": ["066de609-b04a-4b30-b46c-32537c7f1f6e"],
                "limit" : {},
                "admin_limit" : {}
            }
        }

class Update_board_schema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    create_date: str = Field(...)
    update_date: str = Field(...)
    pinned: bool = Field(...)
    like: list = Field(...)
    limit: dict = Field(...)
    admin_limit: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "title",
                "content": "content",
                "create_date": "2017-10-13T10:53:53Z",
                "update_date": "2017-10-13T10:53:53Z",
                "pinned": True,
                "like": ["066de609-b04a-4b30-b46c-32537c7f1f6e"],
                "limit" : {"deleted":True},
                "admin_limit" : {"hide":True}
            }
        }


