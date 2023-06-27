from sqlalchemy import Column, Float, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Community(BaseModel):
    id = Column(String(64), primary_key=True)
    symptom = Column(Text)
    date = Column(Date)
    boards = Column(Text)
    manager = Column(String(255))
    image_file = Column(String(255))
    content = Column(Text)

