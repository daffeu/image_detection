import json
from dataclasses import asdict
from typing import Dict, Any

from bson import ObjectId
from bson.json_util import dumps

from models.data.users import User, Task


class UserRepository:

    def __init__(self, db):
        self.users = db["users"]
        self.tasks = db["tasks"]

    def create_user(self, details: Dict):
        try:
            user = self.users.find_one({"username": details["username"]})
            if user:
                return False
            else:
                self.users.insert_one(details)
        except Exception:
            return False
        return True

    def create_task(self, details: Dict):
        try:
            self.tasks.insert_one(details)
        except Exception:
            return False
        return True

    def delete_task(self, id: ObjectId):
        try:
            self.tasks.delete_one({"_id": id})
        except Exception:
            return False
        return True

    def update_task(self, details: Dict[str, Any]):
        pass

    def get_user(self, username: str):
        user = self.users.find_one({"username": username})
        return asdict(User(**json.loads(dumps(user))))

    def get_task(self, id: str):
        task = self.tasks.find_one({"_id": ObjectId(id)})
        return asdict(Task(**json.loads(dumps(task))))

    def get_all_tasks(self, user_id: str):
        all_tasks = [asdict(Task(**json.loads(dumps(task))))
                     for task in self.tasks.find({'owner_id': user_id})]
        return all_tasks
