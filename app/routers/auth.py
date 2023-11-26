from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import (
    auth as auth_schema,
    user as user_schema,
    settings as setting_schema,
    password as password_schema,
)
from ..controllers import auth as auth_controller
from ..utils.setup import config
from ..services.auth import AuthService


router = APIRouter(prefix=config.AUTH_URL, tags=["Authentication"])


@router.post("/sign-up", response_model=auth_schema.AuthResponse)
async def signup(user_data: auth_schema.SignUpSchema):
    return auth_controller.AuthController.sign_up(user_data)


@router.post("/token", response_model=dict)
def token(user_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_schema.LoginSchema(
        email=user_data.username, password=user_data.password
    )
    return auth_controller.AuthController.login_in_doc(user)


@router.post("/login", response_model=auth_schema.AuthResponse)
def login(user_data: auth_schema.LoginSchema):
    print("Login: ", user_data)
    return auth_controller.AuthController.login_in(user_data)


@router.post("/social-auth", response_model=auth_schema.AuthResponse)
def social_auth(user_data: auth_schema.SocialAuthSchema):
    return auth_controller.AuthController.social_auth(user_data)


@router.post("/subscribe", response_model=auth_schema.SubscribeResponse)
def subscribe(sub_data: auth_schema.SubscribeSchema):
    return auth_controller.AuthController.subscribe(sub_data)


@router.patch("/user/setting", response_model=setting_schema.UpdateSettingsResponse)
def update_settings(
    data: setting_schema.SettingsSchema,
    user_id: str = Depends(AuthService.get_current_user_id),
):
    return auth_controller.AuthController.update_settings(data, user_id)


@router.get("/user/setting", response_model=setting_schema.GetSettingsResponse)
def get_settings(user_id: str = Depends(AuthService.get_current_user_id)):
    return auth_controller.AuthController.get_settings(user_id)


@router.post("/user/delete", response_model=user_schema.DeleteUserResponse)
def delete_user(
    data: user_schema.DeleteUserSchema,
    user_id: str = Depends(AuthService.get_current_user_id),
):
    return auth_controller.AuthController.delete_user(data, user_id)


@router.post(
    "/user/password/request-reset",
    response_model=password_schema.RequestPasswordResetResponse,
)
def request_password_reset(data: password_schema.RequestPasswordResetSchema):
    return auth_controller.AuthController.request_password_reset(data)


@router.post(
    "/user/validate-token", response_model=password_schema.ValidateTokenResponse
)
def validate_token(data: password_schema.ValidateTokenSchema):
    return auth_controller.AuthController.validate_token(data)


@router.post(
    "/user/password/reset", response_model=password_schema.ResetPasswordResponse
)
def reset_password(data: password_schema.ResetPasswordSchema):
    return auth_controller.AuthController.reset_password(data)
