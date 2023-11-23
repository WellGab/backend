from pymongo import MongoClient


class MongoDBActions:
    def __init__(self, collection_name, db):
        self.db = db
        self.collection = self.db[collection_name]

    def create(self, data):
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"Error during create operation: {e}")
            return None

    def read(self, query=None):
        try:
            if query is None:
                result = self.collection.find()
            else:
                result = self.collection.find(query)
            return list(result)
        except Exception as e:
            print(f"Error during read operation: {e}")
            return None

    def update(self, query, new_values):
        try:
            result = self.collection.update_many(query, {'$set': new_values})
            return result.modified_count
        except Exception as e:
            print(f"Error during update operation: {e}")
            return 0

    def delete(self, query):
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error during delete operation: {e}")
            return 0
