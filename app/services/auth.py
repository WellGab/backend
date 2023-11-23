# from .base import (
#     BaseService,
#     BaseDataManager
# )
from typing import Optional
from passlib.context import CryptContext
from pymongo import *
from mongoengine import *

from ..models.user import User
from ..utils.setup import token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def hash(password: str) -> str:
        """Generate a bcrypt hashed password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verify a password against a hash."""

        return pwd_context.verify(plain_password, hashed_password)

class AuthService(HashingMixin):
    """Authentication service."""

    def create_user(self, email: str, password: str) -> dict:
        hashed_password = self.hash(password)

        user: User = User(email=email, password=hashed_password).save()
        id: str = str(user.id)

        access_token = token.create_access_token(payload= {"user_id": id}) 

        return {
            "user_id": id,
            "token": access_token
        }

    def login_user(self, id: str, password: str, hashed_password: str) -> dict:
        """Verifies login credentials and returns access token."""
        if not self.verify(hashed_password, password):
            return None

        access_token = token.create_access_token(payload= {"user_id": id}) 
        return {
            "user_id": id,
            "token": access_token
        }

class AuthDataManager:
    @staticmethod
    def add_user(self, email: str, pa) -> None:
        """Write user to database."""

        ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()

    def get_user(self, email: str) -> None:
        """Read user from database."""