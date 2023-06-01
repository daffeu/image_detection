from pymongo import MongoClient
from secutiry.settings import MONGO_HOST


def create_db_collections():
    client = MongoClient(f'mongodb://{MONGO_HOST}:27017/')
    try:
        db = client["fast_api"]
        users = db["users"]
        tasks = db["tasks"]
        yield {"users": users, "tasks": tasks}
    finally:
        client.close()
