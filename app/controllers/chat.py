from fastapi import status, HTTPException
from ..schemas import chat as chat_schema
from ..services import chat as chat_service
import json


class ChatController:
    """Chats Controller."""

    @staticmethod
    async def send_message(sid: str, data: str) -> str:
        payload = json.load(str)
        uid = payload['uid'] if payload['uid'] else sid
        message = payload['message']
        response = await chat_service.ChatService.send_message(message)
        chat_service.ChatService.save_conversation(uid, message, response)
        return response

    @staticmethod
    def get_user_conversations(uid: str, page_number: int, page_size: int) -> chat_schema.ConversationResponse:
        if not uid:
            raise HTTPException(status_code=403, detail="Unauthorized user")
        
        count = chat_service.ChatService.get_user_conversations_count(uid)
        conversations = []
        for conversation in chat_service.ChatService.get_user_conversations(uid, page_number, page_size):
            conversations.append(
                chat_schema.Conversation(message= conversation.message, response=conversation.reply)
            )

        message = "conversations retrieved successful"

        prev = page_number - 1 if page_number > 1 else None
        next = page_number + 1 if count - (page_number * page_size) > 0 else None

        if len(conversations) == 0:
            message = "no conversation available"

        return {
            "message": message,
            "status_code": str(status.HTTP_200_OK),
            "data": chat_schema.ConversationResponseData(**{
                "conversations": conversations,
                "count": count,
                "prev": prev,
                "next": next,
            }),
        }
