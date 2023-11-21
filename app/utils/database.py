import motor.motor_asyncio
from .config import config

def create_db():
        client = motor.motor_asyncio.AsyncIOMotorClient(config.database.dsn)
        db = client.wellgab
        return db