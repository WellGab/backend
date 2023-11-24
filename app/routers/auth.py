from fastapi import Response, status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..schemas import auth as auth_schema
from ..controllers import auth as auth_controller

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/sign-up", response_model=auth_schema.AuthResponse)
async def signup(user_data: auth_schema.SignUpSchema):
    return auth_controller.AuthController.sign_up(user_data)


@router.post("/login", response_model=auth_schema.AuthResponse)
def login(user_data: auth_schema.LoginSchema):
    return auth_controller.AuthController.login_in(user_data)


@router.post("/social-auth", response_model=auth_schema.AuthResponse)
def login(user_data: auth_schema.SocialAuthSchema):
    return auth_controller.AuthController.social_auth(user_data)
