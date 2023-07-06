from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Disease(BaseModel):
    id = Column(String(64), primary_key=True)
    disease = Column(String(255))
    diagnosis = Column(String(255))
    symptom = Column(String(1024))
    area = Column(String(1024))
    occur_pattern = Column(String(1024))
    ages = Column(String(255))
    sex = Column(String(16))
    queationaire = Column(Text)
