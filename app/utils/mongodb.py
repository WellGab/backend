from pymongo import MongoClient


class Mongodb():

    def __init__(self, dsn: str, db: str):
        self.db_name = db
        self.conn = MongoClient(dsn)
        # print("///////////////////////////////////////////////// conn ", self.conn)
        self.db = self.conn[db]
        # print("///////////////////////////////////////////////// db ", self.db)

    def get_db(self):
        return self.db

    def get_conn(self):
        return self.conn
