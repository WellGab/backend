from fastapi import status, HTTPException
from ..schemas import chat as chat_schema
from ..models import chat as chat_models
from ..services import chat as chat_service, user as user_service
import json
import bson
import uuid
from datetime import datetime


class ChatController:
    """Chats Controller."""

    @staticmethod
    def create_chat(user_id, req_data: chat_schema.CreateChatSchema) -> chat_schema.CreateChatResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        chatTuple = chat_service.ChatModelService.create_chat(
            user, req_data.topic)
        id = chatTuple[0]
        topic = chatTuple[1]

        if id == "":
            raise HTTPException(status_code=500, detail="chat not created")

        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
            "data": chat_schema.CreateChatResponseData(
                **{"id": id,
                   "topic": topic,
                   },
            )
        }

    @staticmethod
    def get_chats(user_id: str, page_number: int, page_size: int) -> chat_schema.ChatResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")
        chats = chat_service.ChatModelService.get_chats_by_user(
            user, page_number, page_size)

        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
            "data": chats
        }

    @staticmethod
    def get_chat(chat_id: str) -> chat_schema.ChatResponse:
        chat = chat_service.ChatModelService.get_chat_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=400, detail="chat not found")

        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
            "data": chat
        }

    @staticmethod
    def update_chat(user_id: str, chat_id: str, req: chat_schema.UpdateChatSchema) -> chat_schema.ChatResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        chat = chat_service.ChatModelService.get_chat_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=400, detail="chat not found")

        if user.id != chat.user.id:
            raise HTTPException(
                status_code=403, detail="not authorized to update chat")

        conversations: list[chat_models.Conversations] = []

        for conv in req.conversations:
            conversation = chat_models.Conversations(uid=bson.ObjectId(),
                                                     user=user,
                                                     message=conv.message,
                                                     reply=conv.reply,
                                                     created_at=datetime.now())
            conversations.append(conversation)

        chat = chat_service.ChatModelService.update_chat(
            chat, req.topic, conversations)
        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
            "data": chat
        }

    @staticmethod
    def delete_chat(user_id: str, chat_id: str) -> chat_schema.ChatResponse:
        user = user_service.UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user not found")

        chat = chat_service.ChatModelService.get_chat_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=400, detail="chat not found")

        if user.id != chat.user.id:
            raise HTTPException(
                status_code=403, detail="not authorized to delete chat")

        chat = chat_service.ChatModelService.delete_chat(chat)
        if not chat:
            raise HTTPException(
                status_code=500, detail="error occured deleting chat")
        return {
            "message": "Successful",
            "status_code": str(status.HTTP_200_OK),
        }

    @ staticmethod
    async def send_message(sid: str, chat_id: str, message: str) -> str:
        chat = chat_service.ChatModelService.get_chat_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=400, detail="chat not found")

        response = await chat_service.ChatService.interact(message, chat.conversations)
        topic: str = chat.topic
        if topic == "" or ("new" in topic.lower() and "chat" in topic.lower()):
            topic = await chat_service.ChatService.get_topic(message)

        conversation = chat_models.Conversations(uid=bson.ObjectId(),
                                                 user=chat.user,
                                                 message=message,
                                                 reply=response,
                                                 created_at=datetime.now())

        chat = chat_service.ChatModelService.update_chat(
            chat, topic, [conversation])
        return response

    @ staticmethod
    def get_user_conversations(uid: str, page_number: int, page_size: int) -> chat_schema.ConversationResponse:
        if not uid:
            raise HTTPException(status_code=403, detail="Unauthorized user")

        count = chat_service.ChatService.get_user_conversations_count(uid)
        conversations = []
        for conversation in chat_service.ChatService.get_user_conversations(uid, page_number, page_size):
            conversations.append(
                chat_schema.Conversation(
                    message=conversation.message, response=conversation.reply)
            )

        message = "conversations retrieved successful"

        prev = page_number - 1 if page_number > 1 else None
        next = page_number + 1 if count - \
            (page_number * page_size) > 0 else None

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
