from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from .. import model
from .. import schemas
from ..auth import verify_password, get_password_hash
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])

async def get_current_user(db: Session = Depends(get_db), x_user_id: int = Header(None, alias="X-User-ID")):
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID required in X-User-ID header",
        )
    user = db.query(model.User).filter(model.User.id == x_user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User ID",
        )
    return user

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.emailID == user.emailID).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = model.User(
        emailID=user.emailID,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.emailID == login_data.emailID).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return {"user_id": user.id, "full_name": user.full_name, "email": user.emailID}

@router.get("/profile", response_model=schemas.UserResponse)
def read_user_profile(current_user: model.User = Depends(get_current_user)):
    return current_user

@router.put("/profile/update", response_model=schemas.UserResponse)
def update_user_profile(
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(model.User).all()
