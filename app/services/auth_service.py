from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = UserRepository.get_user_by_email(db, email)
        if user and AuthService.verify_password(password, user.hashed_password):
            return user
        return None