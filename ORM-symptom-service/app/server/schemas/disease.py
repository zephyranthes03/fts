import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel
from app.config.config import settings

class DiseaseSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

class UpdateDiseaseModel(BaseModel):
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }


