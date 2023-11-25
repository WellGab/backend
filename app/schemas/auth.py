from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class SocialAuthSchema(BaseModel):
    token: str


class AuthResponseData(BaseModel):
    user_id: str
    token: str


class AuthResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[AuthResponseData]


class SubscribeSchema(BaseModel):
    email: EmailStr


class SubscribeResponse(BaseModel):
    message: str
    status_code: int
