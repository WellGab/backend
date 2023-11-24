from fastapi import status, HTTPException
from ..schemas import chat as chat_schema
from ..services import chat as chat_service
from ..services import user as user_service


class ChatController:
    """Chats Controller."""

    @staticmethod
    async def send_message(uid: str, message: str) -> str:
        response = await chat_service.ChatService.send_message(message)
        return response

   