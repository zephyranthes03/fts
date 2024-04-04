import uuid
from typing import Optional

from pydantic import BaseModel, Field
from app.server.schemas.common import ErrorResponseModel, ResponseModel

class Llm_result_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    diagnosis: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "diagnosis": "ringworm",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "image_file": "19850109.jpg",
            }
        }

class Update_llm_result_schema(BaseModel):
    # diagnosis: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "image_file": "19850109.jpg",
            }
        }