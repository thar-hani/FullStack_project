from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .. import model as models
from .. import schemas as schemas
from ..dependencies import get_db
from .user import get_current_user

router = APIRouter(prefix="/wishes", tags=["Wishes"])

@router.post("/", response_model=schemas.WishResponse, status_code=status.HTTP_201_CREATED)
def create_wish(
    wish: schemas.WishCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    wish_dict = wish.dict()
    if not wish_dict.get("date"):
        wish_dict["date"] = datetime.now().strftime("%Y-%m-%d")
    if not wish_dict.get("time"):
        wish_dict["time"] = datetime.now().strftime("%H:%M:%S")
        
    new_wish = models.Wish(**wish_dict, user_id=current_user.id)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish

@router.get("/", response_model=list[schemas.WishResponse])
def get_my_wishes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Wish).filter(models.Wish.user_id == current_user.id).all()

@router.get("/{wish_id}", response_model=schemas.WishResponse)
def get_wish(
    wish_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    wish = db.query(models.Wish).filter(
        models.Wish.wish_id == wish_id, 
        models.Wish.user_id == current_user.id
    ).first()
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found or access denied")
    return wish

@router.delete("/{wish_id}")
def delete_wish(
    wish_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    wish = db.query(models.Wish).filter(
        models.Wish.wish_id == wish_id, 
        models.Wish.user_id == current_user.id
    ).first()
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found or access denied")
    db.delete(wish)
    db.commit()
    return {"message": "Wish deleted successfully"}
