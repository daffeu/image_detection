from typing import List
from typing import Optional

from fastapi import Request


class TaskCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.url_data: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.description = form.get("description")
        self.url_data = form.get("url_data")

    def is_valid(self):
        if not self.errors:
            return True
        return False