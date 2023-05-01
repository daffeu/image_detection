from datetime import date, datetime
from typing import Dict, List

from pydantic import BaseModel, validator
from bson import ObjectId


class CreateTask(BaseModel):
    title: str
    description: str
    owner_id: str
    create_date: date = datetime.now()
    links: List[str] = list()

    @validator('create_date')
    def create_date_datetime(cls, value):
        return datetime.strptime(value.strftime('%Y-%m-%dT%H:%M:%S'), "%Y-%m-%dT%H:%M:%S")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class CreateUser(BaseModel):
    _id: ObjectId
    username: str
    email: str
    hashed_password: str
    tasks: List[Dict] = list()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }