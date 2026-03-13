from pydantic import BaseModel

class StoryBase(BaseModel):
    date: str
    mood: str
    title: str
    story: str
    tags: str

class StoryCreate(StoryBase):
    pass

class StoryResponse(StoryBase):
    story_id: int
    user_id: int

    class Config:
        from_attributes = True
