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
    applyform: list = Field(...)
    boards: dict = Field(...)
    manager: str = Field(...)
    image_file: str = Field(...)
    comment: str = Field(...)   

    class Config:
        schema_extra = {
            "example": {
                "name": "community name",
                "symptom": "itch,lichenification",
                "date": "2017-10-13T10:53:53Z",
                "applyform": [{'name': {'mandatory': True, 'type':'String','comment':''}}, 
                              {'introduce': {'mandatory': True, 'type':'Text','comment':'한문단 이내'}},
                              {'연령대': {'mandatory': True, 'type':'select','comment':'', 'option':['10대','20대','30대','40대이상']}},
                              {'설문': {'mandatory': True, 'type':'select','comment':'커뮤니티 메너를 잘 지켜주실거죠?','option':['네','아니오']}}
                ],
                "boards": {100:'intro'},
                "manager": "admin",
                "image_file": "http://localhost:8005/community/image/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
                "comment": "comment"
            }
        }

class Update_community_schema(BaseModel):
    name: str = Field(...)
    symptom: str = Field(...)
    date: str = Field(...)
    applyform: list = Field(...)
    boards: dict = Field(...)
    manager: str = Field(...)
    image_file: str = Field(...)
    comment: str = Field(...)   

    class Config:
        schema_extra = {
            "example": {
                "name": "community name",
                "symptom": "itch,lichenification",
                "date": "2017-10-13T10:53:53Z",
                "applyform": [{'name': {'mandatory': True, 'type':'String','comment':''}}, 
                              {'introduce': {'mandatory': True, 'type':'Text','comment':'한문단 이내'}},
                              {'연령대': {'mandatory': True, 'type':'select','comment':'', 'option':['10대','20대','30대','40대이상']}},
                              {'설문': {'mandatory': True, 'type':'select','comment':'커뮤니티 메너를 잘 지켜주실거죠?','option':['네','아니오']}}
                ],
                "boards": {100:'intro'},
                "manager": "admin",
                "image_file": "http://localhost:8005/community/image/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
                "comment": "comment"
            }
        }