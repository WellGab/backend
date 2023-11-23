from fastapi import Response, status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..models import user as auth_models
from ..schemas import auth as auth_schema
# from ..services import auth as auth_service

router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post("/signup/", response_model=dict)
async def signup(user_data: auth_schema.CreateUser):
    # Check if the email already exists
    existing_user = auth_models.User().read({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user document
    new_user = auth_models.User().create(
        {"email": user_data.email, "password": user_data.password})

    if not new_user:
        raise HTTPException(status_code=400, detail="Couldn't create user")

    # Return the created user document
    return {
        "id": new_user,
    }


# @router.post("/login", response_model=auth_schema.LoginResponse)
# def login(res: Response):
#     res.status_code = status.HTTP_200_OK
#     user = auth_service.AuthService().login_user()

#     return {
#         "message": "login successful",
#         "status_code": str(status.HTTP_200_OK),
#         "data": user
#     }
