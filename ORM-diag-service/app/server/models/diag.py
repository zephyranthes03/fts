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
                "detail": "detail_1",
                "queationaire": "queationaire_1",
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
                "detail": "detail_1",
                "queationaire": "queationaire_1",
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
                "detail": "detail_1",
                "inspection": "inspection_1",
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
                "detail": "detail_1",
                "inspection": "inspection_1",
            }
        }

class DiagSchema(BaseModel):
    id: str = Field(...)
    disease: str = Field(...)
    image_file: str = Field(...)
    detail: str = Field(...)
    queationaire: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "disease": "disease_1",
                "image_file": "19850109.jpg",
                "detail": "detail_1",
                "queationaire": "queationaire_1",
            }
        }

class UpdateDiagModel(BaseModel):
    disease: str = Field(...)
    image_file: str = Field(...)
    detail: str = Field(...)
    queationaire: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "disease": "disease_1",
                "image_file": "19850109.jpg",
                "detail": "detail_1",
                "queationaire": "queationaire_1",
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