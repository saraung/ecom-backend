import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.core.security import hash_password, verify_password, create_access_token



logger=logging.getLogger(__name__)
class AuthService:
    @staticmethod
    def register(db:Session,email:str,password:str):
        logger.info(f"Register attempt: {email}")
        if UserRepository.get_by_email(db,email):
            logger.warning(f"Email already registered: {email}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
        user=User(email=email,hashed_password=hash_password(password))
        return UserRepository.create(db,user)
    @staticmethod
    def login(db:Session,email:str,password:str)->str:
        logger.info(f"Login attempt: {email}")
        user=UserRepository.get_by_email(db,email)
        logger.debug(f"User fetched: {user is not None}")
        if not user or not verify_password(password,user.hashed_password):
            logger.warning("Invalid credentials")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")
        logger.debug("Creating JWT token")
        return create_access_token({"sub":user.email})