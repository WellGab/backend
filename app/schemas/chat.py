from pydantic import BaseModel, validator
from pydantic.networks import EmailStr
from typing import List, Optional
# from ..models import chat as chat_models
from datetime import datetime
from .auth import UserSchema
from bson import ObjectId


class MessageSchema(BaseModel):
    message: str


class MessageResponseData(BaseModel):
    message: str
    response: str


class MessageResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[MessageResponseData]


class Conversation(BaseModel):
    message: str
    response: str


class ConversationResponseData(BaseModel):
    conversations: list[Conversation]
    count: int
    prev: Optional[int]
    next: Optional[int]


class ConversationResponse(BaseModel):
    message: str
    status_code: int
    data: ConversationResponseData


class CreateChatSchema(BaseModel):
    topic: str


class CreateAnonChatSchema(BaseModel):
    uid: str
    topic: str


class CreateChatResponseData(BaseModel):
    id: str
    topic: str


class CreateChatResponse(BaseModel):
    message: str
    status_code: int
    data: CreateChatResponseData


class ConversationsSchema(BaseModel):
    uid: str = None
    user: UserSchema = None
    message: str
    reply: str = None
    created_at: datetime = None

    class Config:
        arbitrary_types_allowed = True

    @validator("uid", pre=True)
    def convert_object_ids_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class ChatsSchema(BaseModel):
    id: str = None
    topic: str = None
    user: UserSchema = None
    conversations: List[ConversationsSchema] = []
    created_at: datetime = None

    @validator("id", pre=True)
    def convert_object_ids_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        arbitrary_types_allowed = True


class UpdateChatConversationSchema(BaseModel):
    message: str
    reply: str = None


class UpdateChatSchema(BaseModel):
    topic: str
    conversations: List[UpdateChatConversationSchema]


class ChatResponse(BaseModel):
    message: str
    status_code: int
    data: ChatsSchema = None


class ChatsResponse(BaseModel):
    message: str
    status_code: int
    data: List[ChatsSchema]
