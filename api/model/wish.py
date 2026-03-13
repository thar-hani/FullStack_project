from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Wish(Base):
    __tablename__ = "wishes"

    wish_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    categories = Column(String)
    wishes = Column(String)
    date = Column(String)
    time = Column(String)
    status = Column(String, default="Pending")               
    created_at = Column(DateTime, server_default=func.now()) 

    owner = relationship("User", back_populates="wishes")