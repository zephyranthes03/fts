from typing import Optional

from pydantic import BaseModel, Field

class DiseaseSchema(BaseModel):
    id: str = Field(...)
    disease: str = Field(...)
    detail: str = Field(...)
    queationaire: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "disease": "disease_1",
                "detail": "detail",
                "queationaire": "queationaire",
            }
        }

class UpdateDiseaseModel(BaseModel):
    disease: str = Field(...)
    detail: str = Field(...)
    queationaire: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "disease": "disease_1",
                "detail": "detail",
                "queationaire": "queationaire",
            }
        }

class SampleImageSchema(BaseModel):
    id: str = Field(...)
    image_file: str = Field(...)
    detail: str = Field(...)
    inspection: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "image_file": "19850109.jpg",
                "detail": "detail",
                "inspection": "inspection",
            }
        }

class UpdateSampleImageModel(BaseModel):
    image_file: str = Field(...)
    detail: str = Field(...)
    inspection: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image_file": "19850109.jpg",
                "detail": "detail",
                "inspection": "inspection",
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