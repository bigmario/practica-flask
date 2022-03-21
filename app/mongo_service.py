from flask_pymongo import PyMongo


class MongoConn:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def get_users(self):
        return self.mongo.db.users.find()

    def get_user(self, user_id):
        return self.mongo.db.users.find_one({"_id": user_id})
