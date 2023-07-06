import uuid
from typing import Optional
from pydantic import BaseModel, Field

from app.server.schemas.common import ErrorResponseModel, ResponseModel

class Disease_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    disease: str = Field(...)
    diagnosis: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    image_file: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "disease": "ringworm",
                "diagnosis": "ringworm",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

class Update_disease_schema(BaseModel):
    disease: str = Field(...)
    diagnosis: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "disease": "ringworm",
                "diagnosis": "ringworm",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "image_file": "19850109.jpg",
            }
        }


