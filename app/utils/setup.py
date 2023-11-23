from .config import Configuration
from .mongodb import Mongodb
from .token import Token

config = Configuration()
mongo = Mongodb(f'{config.MONGO_URI}{config.DB_NAME}', config.DB_NAME)
conn = mongo.get_conn()
db = mongo.get_db()

token = Token(config)
