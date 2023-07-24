from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Log_user(BaseModel):
    community_id = Column(String(64))
    # user_id = Column(String(64))
    date = Column(Date)
    action = Column(String(64))
    detail = Column(Text)

