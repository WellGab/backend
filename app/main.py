from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .routers import auth

app = FastAPI()

from app.version import __version__


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


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)