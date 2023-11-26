from pydantic import BaseModel, validator
from pydantic.networks import EmailStr
from bson import ObjectId


class UserSchema(BaseModel):
    id: str
    email: EmailStr

    @validator("id", pre=True)
    def convert_object_ids_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        arbitrary_types_allowed = True


class DeleteUserSchema(BaseModel):
    password: str


class DeleteUserResponse(BaseModel):
    message: str
    status_code: int
