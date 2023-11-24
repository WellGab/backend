from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional

class MessageSchema(BaseModel):
    message: str

class MessageResponseData(BaseModel):
    message: str
    response: str

class MessageResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[MessageResponseData]