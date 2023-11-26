from fastapi import HTTPException
import socketio
from .controllers import chat as chat_controller
from .services.auth import AuthService
from .services.chat import ChatModelService, AnonChatModelService
from .utils.setup import token as tk
from .utils.setup import config


class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, sio_server: socketio.AsyncServer, namespace=None):
        super().__init__(namespace=namespace)
        self.sio_server = sio_server

    async def send_error(self, sid, message):
        await self.sio_server.emit(
            event="error", data=message, namespace=self.namespace, room=sid
        )

    async def on_connect(self, sid, environ, auth):
        print(f"{sid}: connected")
        print(f"{sid}: environ {environ}")
        print(f"connected {sid}: {auth}")

        (id, st) = authenticate_socket_connection(auth)
        if not st:
            self.enter_room(sid, sid)
            # await self.send_error(sid, "not authenticated")
            return

        self.enter_room(sid, id)

    async def on_join(self, sid, data):
        print("joining room")
        auth = data.get("auth", None)
        (id, st) = authenticate_socket_connection(auth)
        # if not st:
        #     self.enter_room(sid, sid)
        #     await self.send_error(sid, "not authenticated")
        #     return
        room: str
        try:
            room = data.get("room")
        except Exception as e:
            self.enter_room(sid, sid)
            await self.send_error(sid, "room not provided")
            return

        chat = (
            ChatModelService.get_chat_by_id(room)
            if st
            else AnonChatModelService.get_anon_chat_by_id(room)
        )
        if not chat:
            self.enter_room(sid, sid)
            await self.send_error(sid, "invalid chat")
            return

        self.enter_room(sid, room, namespace=self.namespace)
        print(f"{sid} joined room: {room}")

    async def on_leave(self, sid, data):
        room: str
        try:
            room = data.get("room")
        except Exception as e:
            self.enter_room(sid, sid)
            await self.send_error(sid, "room not provided")
            return

        self.leave_room(sid, room)
        print(f"{sid} left room: {room}")

    async def on_message(self, sid, data):
        auth = data.get("auth", None)
        (id, st) = authenticate_socket_connection(auth)

        room: str
        try:
            room = data.get("room")
        except Exception as e:
            self.enter_room(sid, sid)
            await self.send_error(sid, "room not provided")
            return

        message: str
        try:
            message = data.get("message")
        except Exception as e:
            pass

        try:
            response = (
                await chat_controller.ChatController.send_message(sid, room, message)
                if (st)
                else await chat_controller.AnonChatController.send_anon_message(
                    sid, room, message
                )
            )
            await self.sio_server.emit(
                event="response", data=response, namespace=self.namespace, room=room
            )
        except HTTPException as e:
            await self.send_error(sid, e.detail)
        except Exception as e:
            await self.send_error(sid, "Something went wrong")

    async def on_disconnect(self, sid):
        print(f"{sid}: disconnected")


def authenticate_socket_connection(auth) -> tuple[str, bool]:
    if not auth:
        return ("", False)

    token: str
    try:
        token = auth.get("token", None)
    except Exception:
        return ("", False)

    if not token:
        return ("", False)
    id: str
    try:
        id = tk.verify_access_token(token)
    except Exception as e:
        print(e)
        return ("", False)

    if not id:
        return ("", False)

    return (id, True)


class ChatServer:
    def __init__(self, app, namespace=None):
        mgr = socketio.AsyncRedisManager(config.REDIS_URL)
        sio_server = socketio.AsyncServer(
            async_mode="asgi", cors_allowed_origins="*", client_manager=mgr
        )
        sio_server.register_namespace(ChatNamespace(sio_server, namespace=namespace))
        self.sio_app = socketio.ASGIApp(socketio_server=sio_server, other_asgi_app=app)
