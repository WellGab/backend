from fastapi import APIRouter, Depends

from ..schemas import chat as chat_schema
from ..controllers import chat as chat_controller
from ..utils.setup import config
from ..services.auth import AuthService

router = APIRouter(prefix=config.CHAT_URL, tags=["Chats"])


# @router.get("/conversations", response_model=chat_schema.ConversationResponse)
# def get_user_conversations(user_id: str = Depends(AuthService.get_current_user_id), page_number: int = 1, page_size: int = 50):
#     return chat_controller.ChatController.get_user_conversations(user_id, page_number, page_size)


@router.post("/chats", response_model=chat_schema.CreateChatResponse)
def create_chat(req_data: chat_schema.CreateChatSchema, user_id: str = Depends(AuthService.get_current_user_id)):
    return chat_controller.ChatController.create_chat(user_id, req_data)


@router.get("/chats", response_model=chat_schema.ChatsResponse)
def get_chats(user_id: str = Depends(AuthService.get_current_user_id), page_number: int = 1, page_size: int = 50):
    return chat_controller.ChatController.get_chats(user_id, page_number, page_size)


@router.get("/chats/{chat_id}", response_model=chat_schema.ChatResponse)
def get_chat(chat_id: str, user_id: str = Depends(AuthService.get_current_user_id)):
    return chat_controller.ChatController.get_chat(chat_id)


@router.patch("/chats/{chat_id}", response_model=chat_schema.ChatResponse)
def update_chat(chat_id: str, req_data: chat_schema.UpdateChatSchema, user_id: str = Depends(AuthService.get_current_user_id)):
    return chat_controller.ChatController.update_chat(user_id, chat_id, req_data)


@router.delete("/chats/{chat_id}", response_model=chat_schema.ChatResponse)
def delete_chat(chat_id: str, user_id: str = Depends(AuthService.get_current_user_id)):
    return chat_controller.ChatController.delete_chat(user_id, chat_id)
