import uuid
from typing import Optional

from pydantic import BaseModel, Field
from app.server.schemas.common import ErrorResponseModel, ResponseModel

class Llm_result_schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    instruction: str = Field(...)
    input: str = Field(...)
    image_base64: str = Field(...)
    output: str = Field(...)
    feedback: int = Field(...)
    feedback_content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "instruction": "instruction text",
                "input": "input text",
                "image_base64": "image base64 text",
                "output": "output text",
                "feedback": 2,
                "feedback_content": ""
            }
        }

class Update_llm_result_schema(BaseModel):
    instruction: str = Field(...)
    input: str = Field(...)
    image_base64: str = Field(...)
    output: str = Field(...)
    feedback: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "instruction": "instruction text",
                "input": "input text",
                "image_base64": "image base64 text",
                "output": "output text",
                "feedback": 1,
                "feedback_content": ""
            }
        }