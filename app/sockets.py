import socketio
import uuid
from .controllers import chat as chat_controller
from .services.auth import AuthService
from .services.chat import ChatModelService
from .utils.setup import token as tk


class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, sio_server: socketio.AsyncServer, namespace=None):
        super().__init__(namespace=namespace)
        self.sio_server = sio_server

    def on_connect(self, sid, environ, auth):
        print(f"{sid}: connected")
        print(f"{sid}: environ {environ}")
        print(f"connected {sid}: {auth}")

        (id, st) = authenticate_socket_connection(auth)
        if not st:
            self.enter_room(sid, uuid.uuid4().hex)
            return

        self.enter_room(sid, id)

    async def on_join(self, sid, data):
        print("emitted join", data)
        auth = data.get("auth")
        (id, st) = authenticate_socket_connection(auth)
        print("emitted join 1", id, st)
        if not st:
            self.enter_room(sid, uuid.uuid4().hex)
            return
        print("emitted join 2")
        room = data.get("room")
        chat = ChatModelService.get_chat_by_id(room)
        print("emitted join 3")
        if not chat:
            self.enter_room(sid, uuid.uuid4().hex)
            return

        print("emitted join 4")
        self.enter_room(sid, room)
        print(f"{sid} joined room: {room}")

    async def on_leave(self, sid, room):
        self.leave_room(sid, room)
        print(f"{sid} left room: {room}")

    async def on_message(self, sid, data):
        # response = await chat_controller.ChatController.send_message(sid, data)
        response = "I got the message: " + str(data)
        await self.sio_server.emit(
            event="response", data=response, namespace=self.namespace, room=sid
        )

    def on_disconnect(self, sid):
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
        sio_server = socketio.AsyncServer(
            async_mode="asgi", cors_allowed_origins="*")
        sio_server.register_namespace(
            ChatNamespace(sio_server, namespace=namespace))
        self.sio_app = socketio.ASGIApp(
            socketio_server=sio_server, other_asgi_app=app)
