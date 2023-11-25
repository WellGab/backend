import socketio
import uuid
from .controllers import chat as chat_controller
from .services.auth import AuthService


class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, sio_server: socketio.AsyncServer, namespace=None):
        super().__init__(namespace=namespace)
        self.sio_server = sio_server

    def on_connect(self, sid, environ, auth):
        print(f"{sid}: connected")
        print(f"{sid}: {environ}")
        print(f"{sid}: {auth}")

        if auth:
            token = auth.get("token", None)
            if token:
                user = AuthService.get_current_sio_user(token)
                if user:
                    self.enter_room(sid, user.id)
                self.disconnect(sid)

        self.enter_room(sid, uuid.uuid4().hex)

    async def on_message(self, sid, data):
        print(f"message|{sid}: ", data)
        response = await chat_controller.ChatController.send_message(sid, data)
        await self.sio_server.emit(
            event="response", data=data, namespace=self.namespace, room=sid
        )

    def on_disconnect(self, sid):
        print(f"{sid}: disconnected")


class ChatServer:
    def __init__(self, app, namespace=None):
        sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
        sio_server.register_namespace(ChatNamespace(sio_server, namespace=namespace))
        self.sio_app = socketio.ASGIApp(socketio_server=sio_server, other_asgi_app=app)
