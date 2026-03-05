from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return UserRepository.get_user_by_id(db, user_id)

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 20) -> list[User]:
        return UserRepository.get_all_users(db, skip=skip, limit=limit)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        user_data.password = hash_password(user_data.password)
        return UserRepository.create_user(db, user_data)

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return None
        if user_data.password:
            user_data.password = hash_password(user_data.password)
        return UserRepository.update_user(db, user, user_data)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return False
        UserRepository.delete_user(db, user)
        return True