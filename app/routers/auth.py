from fastapi import Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..schemas import auth as auth_schema
from ..services import auth as auth_service

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/login", response_model=auth_schema.LoginResponse)
def login(res: Response):
    res.status_code = status.HTTP_200_OK
    user = auth_service.AuthService().login_user()

    return {
            "message": "login successful",
            "status_code": str(status.HTTP_200_OK),
            "data": user
           }