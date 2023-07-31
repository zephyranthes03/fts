from sqlalchemy import Column, Float, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Community_board(BaseModel):
    kind = Column(String(64))
    name = Column(String(256))
    comment = Column(Text)
    condition = Column(String(1024))
    blacklist = Column(Text)
    writelist = Column(Text)
    manager = Column(Text)
    community = Column(String(64), primary_key=True)
    limit = Column(Text)
    
class Community(BaseModel):
    name = Column(String(255))
    symptom = Column(Text)
    date = Column(Date)
    boards = Column(Text)
    manager = Column(String(255))
    image_file = Column(String(255))
    content = Column(Text)

