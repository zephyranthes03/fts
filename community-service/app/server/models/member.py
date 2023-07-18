from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Member(BaseModel):
    join_date = Column(Date)
    post_count = Column(Integer)
    comment_count = Column(Integer)
    point = Column(Integer)
    level = Column(String(64))
    comment = Column(Text)
    admin_comment = Column(Text)
    symptom = Column(Text)

