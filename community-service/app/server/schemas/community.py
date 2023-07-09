import uuid
from typing import Optional

from pydantic import BaseModel, Field
from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class Community_schema(BaseModel):  
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    symptom: str = Field(...)
    date: str = Field(...)
    boards: str = Field(...)
    manager: str = Field(...)
    image_file = Field(...)
    content = Field(...)   

    class Config:
        schema_extra = {
            "example": {
                "name": "community name",
                "symptom": "itch,lichenification",
                "date": "2017-10-13T10:53:53Z",
                "boards": "{100:'intro',}",
                "manager": "admin",
                "image_file": "http://localhost:8005/community/image/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg"
            }
        }

class Update_community_schema(BaseModel):
    name: str = Field(...)
    symptom: str = Field(...)
    date: str = Field(...)
    boards: str = Field(...)
    manager: str = Field(...)
    image_file = Field(...)
    content = Field(...)   

    class Config:
        schema_extra = {
            "example": {
                "name": "community name",
                "symptom": "itch,lichenification",
                "date": "2017-10-13T10:53:53Z",
                "boards": "{100:'intro',}",
                "manager": "admin",
                "image_file": "http://localhost:8005/community/image/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg"
            }
        }


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

