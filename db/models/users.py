from db.base import Base
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Integer


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
