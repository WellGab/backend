from mongoengine import *


class Mongodb():
    def __init__(self, dsn: str, db: str):
        self.db_name = db
        self.conn = connect(host=dsn, alias='default', w='majority')
        self.db = self.conn[db]

    def get_db(self):
        return self.db

    def get_conn(self):
        return self.conn
