from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TasksBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()
    url_data: Optional[str] = None