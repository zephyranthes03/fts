from sqlalchemy import Column, Float, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Community(BaseModel):
    name = Column(String(255))
    symptom = Column(Text)
    date = Column(Date)
    boards = Column(Text)
    manager = Column(String(255))
    image_file = Column(String(1024))
    content = Column(Text)

