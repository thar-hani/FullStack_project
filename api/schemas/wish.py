from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WishBase(BaseModel):
    categories: str
    wishes: str
    date: Optional[str] = None
    time: Optional[str] = None

class WishCreate(WishBase):
    status: Optional[str] = "Pending"   

class WishResponse(WishBase):
    wish_id: int
    user_id: int
    created_at: datetime                 
    status: str                          

    class Config:
        from_attributes = True