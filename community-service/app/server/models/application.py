from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Application(BaseModel):
    user_id = Column(String(64))
    community_id = Column(String(64))
    request_date = Column(Date)
    accept_date = Column(Date)
    request_form = Column(Text)
    accept_flag = Column(Boolean)
    

