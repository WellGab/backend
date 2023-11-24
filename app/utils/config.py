import os
from dotenv import load_dotenv


class Configuration():

    def __init__(self):
        self._get_env_vars()

    def _get_env_vars(self):
        load_dotenv()
        self.MONGO_URI = os.getenv('MONGO_URI')
        self.DB_NAME = os.getenv('DB_NAME')
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.ALGORITHM = os.getenv('ALGORITHM')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
        self.AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
        self.AUTH0_ALGORITHMS= [os.getenv('AUTH0_ALGORITHM')]
        self.API_AUDIENCE=os.getenv('API_AUDIENCE')

    def _set_non_env_vars(self):
        self.AUTH_URL = "auth"
