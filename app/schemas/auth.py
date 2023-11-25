from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional
from datetime import datetime


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


class UserSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr
    password: str
    auth_channel: str
    created_at: datetime = None
