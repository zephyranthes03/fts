from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Post(BaseModel):
    related_post_id = Column(String(64))
    re_id = Column(String(64))
    title = Column(String(512))
    content = Column(Text)
    create_date = Column(Date)
    update_date = Column(Date)
    pinned = Column(Boolean)
    read_count = Column(Integer),
    like_count = Column(Integer),
    like = Column(Text)
    limit = Column(String(512))
    admin_limit = Column(String(512))
    tag = Column(String(512))

