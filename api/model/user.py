from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    emailID = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    stories = relationship("Story", back_populates="owner")
    todos = relationship("Todo", back_populates="owner")
    wishes = relationship("Wish", back_populates="owner")
