from fastapi import status, HTTPException
from ..schemas import auth as auth_schema
from ..services import auth as auth_service
from ..services import user as user_service
from ..models.user import (
    Users,
    AUTH_CHANNEL_DEFAULT,
    AUTH_CHANNEL_GOOGLE,
    AUTH_CHANNEL_APPLE,
    AUTH_CHANNEL_MICROSOFT,
)
from ..utils.setup import config


class AuthController:
    """Authentication Controller."""

    @staticmethod
    def sign_up(user_data: auth_schema.SignUpSchema) -> auth_schema.AuthResponse:
        """Add user with hashed password to database."""
        # Check if the email already exists
        user_exists: bool = user_service.UserService.user_exists(user_data.email)
        if user_exists:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user document
        new_user = auth_service.AuthService.create_user(
            email=user_data.email,
            password=user_data.password,
            auth_channel=AUTH_CHANNEL_DEFAULT,
        )

        if not new_user:
            raise HTTPException(status_code=400, detail="Couldn't create user")

        return {
            "message": "sign up successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.AuthResponseData(**new_user),
        }

    @staticmethod
    def login_in(user_data: auth_schema.LoginSchema) -> auth_schema.AuthResponse:
        """Verifies login credentials and returns access token."""
        user: Users = user_service.UserService.get_user(user_data.email)

        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")

        if user.auth_channel != AUTH_CHANNEL_DEFAULT:
            raise HTTPException(status_code=400, detail="Sign in with social auth")

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=user_data.password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(status_code=400, detail="Couldn't not log in user")

        return {
            "message": "login successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.AuthResponseData(**user),
        }

    @staticmethod
    def login_in_doc(user_data: auth_schema.LoginSchema) -> auth_schema.AuthResponse:
        """Verifies login credentials and returns access token."""
        user: Users = user_service.UserService.get_user(user_data.email)

        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")

        if user.auth_channel != AUTH_CHANNEL_DEFAULT:
            raise HTTPException(status_code=400, detail="Sign in with social auth")

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=user_data.password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(status_code=400, detail="Couldn't not log in user")

        data = auth_schema.AuthResponseData(**user)

        return {
            "access_token": data.token,
            "token_type": "bearer",
            "expires": f"{config.ACCESS_TOKEN_EXPIRE_MINUTES}",
        }

    @staticmethod
    def social_auth(
        user_data: auth_schema.SocialAuthSchema,
    ) -> auth_schema.AuthResponse:
        """Verifies login credentials and returns access token."""
        if user_data.token == "":
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
                },
            )

        payload: dict = auth_service.AuthService.social_auth(
            auth0_token=user_data.token
        )

        error = payload.get("error")
        if error:
            raise HTTPException(
                status_code=error["code"],
                detail={
                    "message": error["message"],
                    "description": error["description"],
                },
            )

        email = payload["email"]
        sub = payload["sub"]

        auth_channel: str

        if "google" in sub:
            auth_channel = AUTH_CHANNEL_GOOGLE
        elif "apple" in sub:
            auth_channel = AUTH_CHANNEL_APPLE
        elif "windows" in sub:
            auth_channel = AUTH_CHANNEL_MICROSOFT
        else:
            raise HTTPException(status_code=400, detail="Invalid auth subscriber")

        password = f"{auth_channel}.{email}|wellgab2024"

        user: Users = user_service.UserService.get_user(email)

        if not user:
            new_user = auth_service.AuthService.create_user(
                email=email, password=password, auth_channel=auth_channel
            )

            if not new_user:
                raise HTTPException(status_code=400, detail="Couldn't create user")

            return {
                "message": "sign up successful",
                "status_code": str(status.HTTP_200_OK),
                "data": auth_schema.AuthResponseData(**new_user),
            }

        if user.auth_channel != auth_channel:
            raise HTTPException(status_code=400, detail="Invalid auth subscriber")

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(status_code=400, detail="Couldn't not log in user")

        return {
            "message": "login successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.AuthResponseData(**user),
        }
