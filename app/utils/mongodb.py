from pymongo import MongoClient


class Mongodb():

    def __init__(self, dsn: str, db: str):
        self.conn = MongoClient(dsn)
        self.db = self.conn[db]

    def get_db(self):
        return self.db
