from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Story(Base):
    __tablename__ = "stories"

    story_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(String)
    mood = Column(String)
    title = Column(String)
    story = Column(Text)
    tags = Column(String)

    owner = relationship("User", back_populates="stories")
