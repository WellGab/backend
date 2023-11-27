from fastapi import status, HTTPException
from ..schemas import (auth as auth_schema,
                       user as user_schema, settings as settings_schema, password as password_schema)
from ..services import (
    auth as auth_service,
    user as user_service,
    subscribe as subscriber_service,
    settings as setting_service,
    mail as mail_service,
    validation_token as vtoken_service
)
from ..models.user import (
    Users,
    AUTH_CHANNEL_DEFAULT,
    AUTH_CHANNEL_GOOGLE,
    AUTH_CHANNEL_APPLE,
    AUTH_CHANNEL_MICROSOFT,
)
from ..models.validation_token import ValidationToken, TokenTypeEnum
from ..models import settings as settings_models
from ..utils.setup import config


class AuthController:
    """Authentication Controller."""

    @staticmethod
    def sign_up(user_data: auth_schema.SignUpSchema) -> auth_schema.AuthResponse:
        """Add user with hashed password to database."""
        # Check if the email already exists
        user_exists: bool = user_service.UserService.user_exists(
            user_data.email)
        if user_exists:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Create user document
        new_user = auth_service.AuthService.create_user(
            email=user_data.email,
            password=user_data.password,
            auth_channel=AUTH_CHANNEL_DEFAULT,
        )

        if not new_user:
            raise HTTPException(status_code=400, detail="Couldn't create user")

        user = user_service.UserService.get_user_by_id(new_user["user_id"])
        setting_service.SettingsService.create_or_update_setting(
            user=user,
            data=settings_schema.SettingsSchema(**{
                "ninety_days_chat_limit": False,
                "text_size": settings_models.SizeEnum.MEDIUM,
                "display": settings_models.DisplayEnum.LIGHT,
            }))

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
            raise HTTPException(
                status_code=400, detail="Sign in with social auth")

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=user_data.password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(
                status_code=400, detail="Couldn't not log in user")

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
            raise HTTPException(
                status_code=400, detail="Sign in with social auth")

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=user_data.password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(
                status_code=400, detail="Couldn't not log in user")

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
            raise HTTPException(
                status_code=400, detail="Invalid auth subscriber")

        password = f"{auth_channel}.{email}|wellgab2024"

        user: Users = user_service.UserService.get_user(email)

        if not user:
            new_user = auth_service.AuthService.create_user(
                email=email, password=password, auth_channel=auth_channel
            )

            if not new_user:
                raise HTTPException(
                    status_code=400, detail="Couldn't create user")

            return {
                "message": "sign up successful",
                "status_code": str(status.HTTP_200_OK),
                "data": auth_schema.AuthResponseData(**new_user),
            }

        if user.auth_channel != auth_channel:
            raise HTTPException(
                status_code=400,
                detail=f"Please login with {user.auth_channel.replace('-', ' ').title()}",
            )

        # Login user
        id = str(user.id)
        user = auth_service.AuthService.login_user(
            id=id, password=password, hashed_password=user.password
        )

        if not user:
            raise HTTPException(
                status_code=400, detail="Couldn't not log in user")

        return {
            "message": "login successful",
            "status_code": str(status.HTTP_200_OK),
            "data": auth_schema.AuthResponseData(**user),
        }

    @staticmethod
    def subscribe(
        user_data: auth_schema.SubscribeSchema,
    ) -> auth_schema.SubscribeResponse:
        # Check if the email already exists
        subscriber_exists: bool = subscriber_service.SubscribeService.subscriber_exists(
            user_data.email
        )
        if subscriber_exists:
            return {
                "message": "Already Subscribed",
                "status_code": str(status.HTTP_200_OK),
            }

        subscribed = subscriber_service.SubscribeService.create_subscriber(
            email=user_data.email
        )

        if not subscribed:
            raise HTTPException(status_code=500, detail="subscription failed")

        return {
            "message": "Successfully Subscribed",
            "status_code": str(status.HTTP_200_OK),
        }

    @staticmethod
    def delete_user(
        data: user_schema.DeleteUserSchema,
        user_id: str
    ) -> auth_schema.SubscribeResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        if not auth_service.HashingMixin.verify(user.password, data.password):
            raise HTTPException(status_code=400, detail="incorrect password")
        
        subscriber_exists: bool = subscriber_service.SubscribeService.subscriber_exists(user.email)
        if subscriber_exists:
            print("1")
            is_unsubscribed = subscriber_service.SubscribeService.delete_subscriber(user.email)
            if not is_unsubscribed:
                print("2")
                raise HTTPException(status_code=400, detail="deleting user failed")

        is_deleted = user_service.UserService.delete_user(user)
        if not is_deleted:
            if subscriber_exists:
                subscriber_service.SubscribeService.create_subscriber(
                    email=user.email
                )
            raise HTTPException(status_code=400, detail="deleting user failed")

        return {
            "message": "Successfully deleted account",
            "status_code": str(status.HTTP_200_OK),
        }

    @staticmethod
    def update_settings(
        data: settings_schema.SettingsSchema,
        user_id: str
    ) -> settings_schema.UpdateSettingsResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        setting = setting_service.SettingsService.create_or_update_setting(
            user, data)

        if not setting:
            raise HTTPException(
                status_code=400, detail="setting update failed")

        return {
            "message": "Successfully updated settings",
            "status_code": str(status.HTTP_200_OK),
        }

    @staticmethod
    def get_settings(
        user_id: str
    ) -> settings_schema.UpdateSettingsResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        setting = setting_service.SettingsService.get_setting_by_user(user)
        if not setting:
            setting = setting_service.SettingsService.create_or_update_setting(
                user, settings_schema.SettingsSchema(**{
                    "ninety_days_chat_limit": False,
                    "text_size": settings_models.SizeEnum.MEDIUM,
                    "display": settings_models.DisplayEnum.LIGHT,
                }))

        if not setting:
            raise HTTPException(
                status_code=400, detail="setting not found")

        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
            "data": setting
        }

    @staticmethod
    def request_password_reset(
        data: password_schema.RequestPasswordResetSchema
    ) -> password_schema.RequestPasswordResetResponse:
        user = user_service.UserService.get_user(data.email)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        token = vtoken_service.ValidationTokenService.create_token(
            user, TokenTypeEnum.PASSWORDRESET)

        sent = mail_service.MailService.send_mail(
            "Password Reset", user.email, {"code": token.token}, "reset_password.html")

        if not sent:
            raise HTTPException(
                status_code=400, detail="error sending password reset otp")
        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK)
        }

    @staticmethod
    def validate_token(
        data: password_schema.ValidateTokenSchema
    ) -> password_schema.ValidateTokenResponse:
        user = user_service.UserService.get_user(data.email)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        token = vtoken_service.ValidationTokenService.get_token(
            user, data.token)
        if not token:
            raise HTTPException(
                status_code=400, detail="invalid token")

        return {
            "message": "token valid",
            "status_code": str(status.HTTP_200_OK)
        }

    @staticmethod
    def reset_password(
        data: password_schema.ResetPasswordSchema
    ) -> password_schema.ResetPasswordResponse:
        user = user_service.UserService.get_user(data.email)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        token = vtoken_service.ValidationTokenService.get_token_with_type(
            user, data.token, TokenTypeEnum.PASSWORDRESET)
        if not token:
            raise HTTPException(
                status_code=400, detail="invalid token")

        updated = user_service.UserService.update_password(
            user, data.new_password)

        if not updated:
            raise HTTPException(
                status_code=400, detail="error reseting password")

        vtoken_service.ValidationTokenService.delete_token(token)

        return {
            "message": "password reset successful",
            "status_code": str(status.HTTP_200_OK)
        }
