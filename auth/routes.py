from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.auth.route_login import login_for_access_token
from auth.forms import UserCreateForm, UserLoginForm
from db.repository.auth import create_new_user
from db.session import get_db
from schemas.auth import UserCreate

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = UserLoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = responses.RedirectResponse("/",
                                                  status_code=status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form, db=db)
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
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            email=form.email, password=form.password
        )
        try:
            create_new_user(user=user, db=db)
            return responses.RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate email")
            return templates.TemplateResponse("auth/register.html", form.__dict__)
    return templates.TemplateResponse("auth/register.html", form.__dict__)
