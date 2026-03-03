from sqlalchemy.orm import Session

from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 20) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        db_user = User(
            email=user_data.email,
            hashed_password=user_data.password,  # already hashed by service layer
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()


class UserProfileRepository:
    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: int) -> UserProfile | None:
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def create_profile(db: Session, profile_data: dict) -> UserProfile:
        db_profile = UserProfile(**profile_data)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile