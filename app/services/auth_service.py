import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.models.user import User

logger=logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register():
        pass
    @staticmethod
    def login():
        pass