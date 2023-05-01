from typing import List
from typing import Optional

from fastapi import Request


class TaskCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.links: Optional[List] = list()

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title", "Untitled")
        self.description = form.get("description", "No description")
        self.links = form.get("links").split(', ')

    def is_valid(self):
        if not self.errors and self.links:
            return True
        return False