from pydantic import BaseModel

class PostData(BaseModel):
    symptom_text: str
    base64_image: str

class PutData(BaseModel):
    id: str
    feedback: int
    feedback_content: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    id: str