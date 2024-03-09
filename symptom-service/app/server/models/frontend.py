from pydantic import BaseModel

class PostData(BaseModel):
    symptom_text: str
    base64_image: str

class ApiResponse(BaseModel):
    success: bool
    message: str