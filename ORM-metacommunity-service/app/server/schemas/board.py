import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Board_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    kind: str = Field(...)
    name: str = Field(...)
    comment: str = Field(...)
    condition: str = Field(...)
    blacklist: str = Field(...)
    writelist: str = Field(...)
    manager: str = Field(...)
    community: str = Field(...)
    limit: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "kind": "board",
                "name": "Intro",
                "comment": "Free Intro board for this community",
                "condition": "{}",
                "blacklist": "{}",
                "writelist": "{}",
                "community": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "limit" : "{}"
            }
        }

class Update_board_schema(BaseModel):
    kind: str = Field(...)
    name: str = Field(...)
    comment: str = Field(...)
    condition: str = Field(...)
    blacklist: str = Field(...)
    writelist: str = Field(...)
    manager: str = Field(...)
    community: str = Field(...)
    limit: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "kind": "board",
                "name": "Intro",
                "comment": "Free Intro board for this community",
                "condition": "{}",
                "blacklist": "{}",
                "writelist": "{}",
                "community": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "limit" : "{}"
            }
        }

