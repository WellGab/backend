import socketio
from .controllers import chat as chat_controller

class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, sio_server: socketio.AsyncServer, namespace = None):
        super().__init__(namespace=namespace)
        self.sio_server = sio_server

    def on_connect(self, sid, environ, auth):
        print(f'{sid}: connected')
        print(f'{sid}: {environ}')
        print(f'{sid}: {auth}')

    async def on_message(self, sid, data):
        print(f'message|{sid}: ', data)
        response = chat_controller.ChatController.send_message(sid, data)
        await self.sio_server.emit(event="response", data=response, namespace=self.namespace)

    def on_disconnect(self, sid):
       print(f'{sid}: disconnected')

class ChatServer:
    def __init__(self, app, namespace = None):
        sio_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
        sio_server.register_namespace(ChatNamespace(sio_server, namespace=namespace))
        self.sio_app = socketio.ASGIApp(socketio_server=sio_server, other_asgi_app=app)

