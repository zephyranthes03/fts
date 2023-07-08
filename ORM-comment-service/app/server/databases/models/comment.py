from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Comment(BaseModel):
    post_id = Column(String(64))
    comment_id = Column(String(64))
    content = Column(Text)
    create_date = Column(Date)
    pinned = Column(Boolean)
    like = Column(Text)
    limit = Column(String(512))
    admin_limit = Column(String(512))
