from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseData(BaseModel):
    user_id: int
    token: str


class LoginResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[LoginResponseData]


class CreateUser(BaseModel):
    email: EmailStr
    password: str
