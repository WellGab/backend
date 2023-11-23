from .config import Configuration
from .mongodb import Mongodb

config = Configuration()
mongo = Mongodb(config.MONGO_URI, config.DB_NAME)
conn = mongo.get_conn()
db = mongo.get_db()
