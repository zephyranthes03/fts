from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

class Message(BaseModel):
    sender_id = Column(String(64))
    receiver_id = Column(String(64))
    message_type = Column(String(64))
    content = Column(Text)
    send_date = Column(Date)
    receive_date = Column(Date)
    pinned = Column(Boolean)
