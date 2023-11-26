from pydantic import BaseModel
from pydantic.networks import EmailStr


class RequestPasswordResetSchema(BaseModel):
    email: EmailStr


class RequestPasswordResetResponse(BaseModel):
    message: str
    status_code: int


class ValidateTokenSchema(BaseModel):
    email: EmailStr
    token: str


class ValidateTokenResponse(BaseModel):
    message: str
    status_code: int


class ResetPasswordSchema(BaseModel):
    email: EmailStr
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    message: str
    status_code: int
