from pymongo import MongoClient
from .config import config

def create_db():
        conn = MongoClient(config.database.dsn)
        db = conn.wellgab
        return db