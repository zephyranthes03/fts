import uuid
from typing import Optional

from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel

class Symptom_index_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    disease: str = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)
    email: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "disease": "",
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
                "email": "john_doe1@gmail.com"
            }
        }

class Update_symptom_index_schema(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    disease: str = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)
    email: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                # "id": "test_id",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "disease": "",
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
                "email": "john_doe1@gmail.com"
            }
        }
