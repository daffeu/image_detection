from db.base_class import Base
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Tasks(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date_posted = Column(Date)
    url_data = Column(String, nullable=False)