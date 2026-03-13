from pydantic import BaseModel

class UserBase(BaseModel):
    emailID: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    emailID: str
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
