from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional

class SignUpSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseData(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[LoginResponseData]


class SignUpResponseData(BaseModel):
    user_id: str
    token: str


class SignUpResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[SignUpResponseData]

