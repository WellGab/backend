from fastapi import APIRouter

from ..schemas import chat as chat_schema
from ..controllers import chat as chat_controller
from ..utils.setup import config

router = APIRouter(prefix=config.CHAT_URL, tags=['Chats'])

@router.get("/conversations", response_model=chat_schema.MessageResponse)
async def send_message(data: chat_schema.MessageSchema):
    # uid = ''
    # return chat_controller.ChatController.send_message(uid, data.message)
    return
