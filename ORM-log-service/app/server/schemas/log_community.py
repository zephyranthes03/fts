import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class log_community_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    # community_id:str = Field(...)
    user_id: str = Field(...)
    date: str = Field(...)
    action: str = Field(...)
    detail: dict = Field(...) 

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "date": "2017-10-13T10:53:53Z",
                "action": "read",
                "detail": {"details":"no details"}
            }
        }

class Update_log_community_schema(BaseModel):
    # community_id:str = Field(...)
    user_id: str = Field(...)
    date: str = Field(...)
    action: str = Field(...)
    detail: str = Field(...) 

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "date": "2017-10-13T10:53:53Z",
                "action": "read",
                "detail": {"details":"no details"}
            }
        }

