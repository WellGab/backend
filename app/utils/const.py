import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

AUTH_URL: Final = "auth"


MONGO_URI = os.getenv('MONGO_URI')
REDIS_URL = os.getenv('REDIS_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))