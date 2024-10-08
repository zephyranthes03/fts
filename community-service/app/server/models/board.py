from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Board(BaseModel):
    kind = Column(String(64))
    name = Column(String(256))
    comment = Column(Text)
    condition = Column(String(1024))
    blacklist = Column(Text)
    whitelist = Column(Text)
    manager = Column(Text)
    community_id = Column(String(64))
    limit = Column(Text)
    lastupdatedate = Column(Date)    
