import motor.motor_asyncio

def create_db():
        client = motor.motor_asyncio.AsyncIOMotorClient("MONGODB_URL")
        db = client.wellgab
        return db