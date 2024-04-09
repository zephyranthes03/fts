from sqlalchemy import Column, Float, String, Boolean, Text, Date, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from pydantic import BaseModel, Base64Bytes

class Feedback(Enum):
    SATISFIY_CONFIRMED = "SATISFIY_CONFIRMED"
    SATISFIY = "SATISFIY"
    NO_FEEDBACK = "NO_FEEDBACK" 
    REQUEST_IMPROVEMENT = "REQUEST_IMPROVEMENT"
    REQUEST_PROFESSIONAL_SUPPORT = "REQUEST_PROFESSIONAL_SUPPORT"

class Llm_result(BaseModel):
    # id = Column(String(64), primary_key=True)
    instruction = Column(String(1024))
    input = Column(String(1024))
    image_base64 = Column(LargeBinary)
    output = Column(String(4096))
    feedback = Column(Feedback)
    feedback_content = Column(String(1024))

