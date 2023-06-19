from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.server.databases.base_class import Base

class Disease(Base):
    id = Column(String(45), primary_key=True)
    symptom = Column(String(1024))
    area = Column(String(1024))
    occur_pattern = Column(String(1024))
    ages = Column(String(255))
    sex = Column(String(16))
    diagnosis = Column(String(255))
    queationaire = Column(Text)
