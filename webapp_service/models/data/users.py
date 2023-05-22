from dataclasses import field
from datetime import date, datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import validator
from pydantic.dataclasses import dataclass


class Config:
    arbitrary_types_allowed = True


@dataclass(config=Config)
class Task:
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[str] = None
    create_date: Optional[date] = "1900-01-01T00:00:00"
    links: List = field(default_factory=list)
    _id: ObjectId = field(default=ObjectId())

    @validator('create_date', pre=True)
    def create_date_datetime(cls, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").date()


@dataclass(config=Config)
class User:
    username: str = None
    email: str = None
    hashed_password: str = None
    tasks: List = field(default_factory=list)
    _id: ObjectId = field(default=ObjectId())
