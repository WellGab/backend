from .config import Configuration
from .mongodb import Mongodb

config = Configuration()
conn = Mongodb(config.MONGO_URI, "wellgab")
db = conn.get_db()
