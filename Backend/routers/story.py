from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import model as models
import schemas as schemas
from dependencies import get_db
from routers.user import get_current_user

router = APIRouter(prefix="/stories", tags=["Stories"])

@router.post("/", response_model=schemas.StoryResponse, status_code=status.HTTP_201_CREATED)
def create_story(
    story: schemas.StoryCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_story = models.Story(**story.dict(), user_id=current_user.id)
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return new_story

@router.get("/", response_model=list[schemas.StoryResponse])
def get_my_stories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Story).filter(models.Story.user_id == current_user.id).all()

@router.get("/{story_id}", response_model=schemas.StoryResponse)
def get_story(
    story_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    story = db.query(models.Story).filter(
        models.Story.story_id == story_id, 
        models.Story.user_id == current_user.id
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found or access denied")
    return story

@router.delete("/{story_id}")
def delete_story(
    story_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    story = db.query(models.Story).filter(
        models.Story.story_id == story_id, 
        models.Story.user_id == current_user.id
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found or access denied")
    db.delete(story)
    db.commit()
    return {"message": "Story deleted successfully"}
