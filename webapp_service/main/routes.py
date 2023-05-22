from json import dumps, loads

from fastapi import APIRouter, Request
from fastapi import Depends, status, responses
from fastapi.templating import Jinja2Templates
from channel_box import channel_box
from channel_box import ChannelBoxEndpoint

from db_config.mongo_config import create_db_collections
from main.forms import TaskCreateForm
from models.request.users import CreateTask
from models.utils import json_serialize_date, json_serialize_oid
from producer import methods as producer_methods
from repository.user import UserRepository
from secutiry.secure import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.get('/')
async def index(request: Request,
                db=Depends(create_db_collections),
                current_user=Depends(get_current_user),
                msg: str = None):
    if current_user:
        repo = UserRepository(db)
        tasks = repo.get_all_tasks(current_user['_id']['$oid'])
        tasks = loads(dumps(tasks, default=json_serialize_oid))
        return templates.TemplateResponse(
            "main/main.html", context={"request": request, "tasks": tasks, "msg": msg}
        )
    return responses.RedirectResponse(
        "/login", status_code=status.HTTP_302_FOUND
    )


@router.get('/create-task')
async def create_task(request: Request,
                      current_user=Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse(
            "tasks/create_task.html", {"request": request}
        )
    return responses.RedirectResponse(
        "/login", status_code=status.HTTP_302_FOUND
    )


@router.post('/create-task')
async def create_task(request: Request,
                      current_user=Depends(get_current_user),
                      db=Depends(create_db_collections)):
    if current_user:
        form = TaskCreateForm(request)
        await form.load_data()
        if form.is_valid():
            form.__dict__.update({"owner_id": current_user["_id"]["$oid"]})
            task = CreateTask(**form.__dict__)
            task_dict = task.dict()
            task_json = dumps(task_dict, default=json_serialize_date)
            repo = UserRepository(db)
            result = repo.create_task(loads(task_json))
            if result:
                return responses.RedirectResponse(
                    "/", status_code=status.HTTP_302_FOUND
                )
            else:
                form.__dict__.get("errors").append("Unknown problem :(")
                return templates.TemplateResponse(
                    "tasks/create_task.html", form.__dict__
                )
        return templates.TemplateResponse(
            "tasks/create_task.html", form.__dict__
        )
    return responses.RedirectResponse(
        "/login", status_code=status.HTTP_302_FOUND
    )


@router.get("/details/{task_id}")
def task_detail(task_id: str, request: Request,
                current_user=Depends(get_current_user),
                db=Depends(create_db_collections)):
    if current_user:
        repo = UserRepository(db)
        task = repo.get_task(task_id)
        return templates.TemplateResponse(
            "tasks/detail.html", {"request": request, "task": task}
        )
    return responses.RedirectResponse(
        "/login", status_code=status.HTTP_302_FOUND
    )


class Channel(ChannelBoxEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expires = 16000
        self.encoding = "json"
        self.task_data = {}

    async def on_connect(self, websocket, **kwargs):
        channel_name = websocket.query_params.get("task_id", " ")
        db = create_db_collections()
        self.task_data.update(UserRepository(next(db)).get_task(channel_name[3:]))
        await self.channel_get_or_create(channel_name, websocket)
        await websocket.accept()

    async def on_receive(self, websocket, data):
        message = "Sent for data collection"
        await producer_methods.send_message_to_vk_extractor(self.task_data)
        payload = {
            "message": message
        }
        await self.channel_send(payload, history=True)


router.add_websocket_route(path="/task_ws", endpoint=Channel)
