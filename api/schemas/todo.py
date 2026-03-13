from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str
    date: str
    time: str
    status: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    status: str

class TodoResponse(TodoBase):
    todo_id: int
    user_id: int

    class Config:
        from_attributes = True
