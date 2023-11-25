from fastapi import APIRouter, Depends

from ..schemas import chat as chat_schema
from ..schemas import auth as _schema
from ..controllers import chat as chat_controller
from ..utils.setup import config
from ..services.auth import AuthService
from app.models.user import Users

router = APIRouter(prefix=config.CHAT_URL, tags=["Chats"])


@router.get("/conversations", response_model=dict)
async def send_message(user: Users = Depends(AuthService.get_current_user)):
    # uid = ''
    # return chat_controller.ChatController.send_message(uid, data.message)
    return {"email": user.email}
