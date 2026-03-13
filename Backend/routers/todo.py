from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import model as models
import schemas as schemas
from dependencies import get_db
from routers.user import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_todo = models.Todo(**todo.dict(), user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/", response_model=list[schemas.TodoResponse])
def get_my_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()

@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.todo_id == todo_id, 
        models.Todo.user_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or access denied")
    return todo

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo_status(
    todo_id: int, 
    todo_update: schemas.TodoUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.todo_id == todo_id, 
        models.Todo.user_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or access denied")
    todo.status = todo_update.status
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.todo_id == todo_id, 
        models.Todo.user_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or access denied")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
