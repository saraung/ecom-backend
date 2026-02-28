from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService
from app.core.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user_data)

@router.put("/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, user_data)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(db, user_id)