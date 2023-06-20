from typing import Optional

from pydantic import BaseModel, Field


class Disease_schema(BaseModel):
    id: str = Field(...)
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
                "id": "19850109",
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

class Diagnosis_schema(BaseModel):
    id: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

class Update_diagnosis_schema(BaseModel):
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
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
                "bmi": 20.1,
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

class Symptom_index_Schema(BaseModel):
    id: str = Field(...)
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
    diagnosis: str = Field(...)
    image_file: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "symptom": "itch,lichenification",
                "area": "elbow",
                "occur_pattern": "on-again",
                "ages": "children",
                "sex": "male",
                "bmi": 20.1,
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

class Update_symptom_index_schema(BaseModel):
    symptom: str = Field(...)
    area: str = Field(...)
    occur_pattern: str = Field(...)
    ages: str = Field(...)
    sex: str = Field(...)
    bmi: float = Field(...)
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
                "bmi": 20.1,
                "diagnosis": "ringworm",
                "image_file": "19850109.jpg",
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}