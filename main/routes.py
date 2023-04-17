from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from db.repository.tasks import list_tasks, create_new_task, retreive_task
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends, status, responses
from main.forms import TaskCreateForm
from fastapi.security.utils import get_authorization_scheme_param
from api.auth.route_login import get_current_user_from_token
from db.models.users import User
from schemas.tasks import TasksBase


router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.get('/')
async def index(request: Request, db: Session = Depends(get_db), msg: str = None):
    tasks = list_tasks(db=db)
    return templates.TemplateResponse(
        "main/main.html", context={"request": request, "tasks": tasks, "msg": msg}
    )


@router.get("/details/{id}")
def task_detail(id: int, request: Request, db: Session = Depends(get_db)):
    task = retreive_task(id=id, db=db)
    return templates.TemplateResponse(
        "tasks/detail.html", {"request": request, "task": task}
    )


@router.get('/create-task')
async def create_task(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "tasks/create_task.html", {"request": request}
    )


@router.post('/create-task')
async def create_task(request: Request, db: Session = Depends(get_db)):
    form = TaskCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            print(form.__dict__)
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )
            current_user: User = get_current_user_from_token(token=param, db=db)
            task = TasksBase(**form.__dict__)
            print(task)
            task = create_new_task(task=task, db=db)
            return responses.RedirectResponse(
                f"/details/{task.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in."
            )
            return templates.TemplateResponse("tasks/create_task.html", form.__dict__)
    return templates.TemplateResponse("tasks/create_task.html", form.__dict__)