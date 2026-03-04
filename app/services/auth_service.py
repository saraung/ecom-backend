from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    @staticmethod
    def register(db: Session, email: str, password: str) -> User:
        """Register a new user with hashed password."""
        existing = UserRepository.get_user_by_email(db, email)
        if existing:
            return None  # caller should raise 409
        hashed = hash_password(password)
        user = User(email=email, hashed_password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> str | None:
        """Authenticate user and return JWT access token, or None."""
        user = UserRepository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        token = create_access_token(data={"sub": str(user.id)})
        return token