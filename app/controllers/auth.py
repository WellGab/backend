from fastapi import status, HTTPException
from ..schemas import auth as auth_schema
from ..services import auth as auth_service
from ..services import user as user_service
from ..models.user import User


class AuthController:
    """Authentication Controller."""

    # def __init__(self) -> None:
    # self.db = db
    @staticmethod
    def sign_up(user_data: auth_schema.SignUpSchema) -> auth_schema.SignUpResponse:
        """Add user with hashed password to database."""
        # Check if the email already exists
        user_exists: bool = user_service.UserService.user_exists(
            user_data.email)
        if user_exists:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Create user document
        new_user = auth_service.AuthService.create_user(
            email=user_data.email, password=user_data.password)

        if not new_user:
            raise HTTPException(status_code=400, detail="Couldn't create user")

        return {
            "message": "sign up successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.SignUpResponseData(**new_user)
        }

    @staticmethod
    def login_in(user_data: auth_schema.LoginSchema) -> auth_schema.LoginResponse:
        """Verifies login credentials and returns access token."""
        user: User = user_service.UserService.get_user(user_data.email)

        # Create user document
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=user_data.password, hashed_password=user.password)

        if not user:
            raise HTTPException(status_code=400, detail="Couldn't create user")

        return {
            "message": "login successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.LoginResponseData(**user)
        }
