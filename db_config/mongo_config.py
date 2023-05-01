from pymongo import MongoClient


def create_db_collections():
    client = MongoClient('mongodb://localhost:27017/')
    try:
        db = client["fast_api"]
        users = db["users"]
        tasks = db["tasks"]
        yield {"users": users, "tasks": tasks}
    finally:
        client.close()