from fastapi import APIRouter, Request
from fastapi import Depends, status, responses
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from db_config.mongo_config import create_db_collections
from secutiry.secure import get_current_user
from repository.user import UserRepository
from models.request.users import CreateTask
from json import dumps, loads
from datetime import date, datetime
from bson import ObjectId

from main.forms import TaskCreateForm

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


def json_serialize_date(obj):
    if isinstance(obj, (date, datetime)):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError("The type %s not serializable." % type(obj))


def json_serialize_oid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("The type %s not serializable." % type(obj))


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

