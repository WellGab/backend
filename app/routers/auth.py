from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import auth as auth_schema
from ..controllers import auth as auth_controller
from ..utils.setup import config


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
