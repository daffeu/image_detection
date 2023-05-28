from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi import responses
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from api.auth.route_login import login_for_access_token
from auth.forms import UserCreateForm, UserLoginForm
from db_config.mongo_config import create_db_collections
from models.request.users import CreateUser
from repository.user import UserRepository
from secutiry.secure import get_password_hash
from json import dumps, loads


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, db=Depends(create_db_collections)):
    form = UserLoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
            login_for_access_token(response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register(request: Request, db=Depends(create_db_collections)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = CreateUser(username=form.username,
                          email=form.email,
                          hashed_password=get_password_hash(form.password))
        user_dict = user.dict()
        user_json = dumps(user_dict)
        user_repo = UserRepository(db)
        result = user_repo.create_user(loads(user_json))
        if result:
            return responses.RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        else:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("auth/register.html", form.__dict__)
    return templates.TemplateResponse("auth/register.html", form.__dict__)
