from pymongo import MongoClient
from .config import config

conn = MongoClient(config.database.dsn)

db = conn.wellgab

