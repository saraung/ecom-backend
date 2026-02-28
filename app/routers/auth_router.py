from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.core.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    return AuthService.register(db, email, password)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    token = AuthService.login(db, email, password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}