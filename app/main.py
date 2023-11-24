from app.version import __version__
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ( auth, chat )

from .sockets import ChatServer

from .utils.setup import config



app = FastAPI(
    title="WellGab",
    description="An AI powered medical diagnosis app",
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(config.ROOT_PATH)
async def root():
    return {"message": "WellGab"}

app.include_router(prefix=config.ROOT_PATH, router=auth.router)
app.include_router(prefix=config.ROOT_PATH, router=chat.router)

chat_server = ChatServer(app, f'{config.ROOT_PATH}/chats')
sio_asgi_app = chat_server.sio_app

app.add_route(f'{config.ROOT_PATH}/chats', route=sio_asgi_app, methods=["GET", "POST"])
app.add_websocket_route("/socket.io/", sio_asgi_app)