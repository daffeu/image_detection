from datetime import timedelta

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from db_config.mongo_config import create_db_collections
from secutiry.secure import authenticate, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from models.request.tokens import Token
from repository.user import UserRepository


router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db=Depends(create_db_collections)
):
    username = form_data.username
    password = form_data.password
    repo: UserRepository = UserRepository(db)
    account = repo.get_user(username)
    if not authenticate(password, account.get('hashed_password')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": form_data.username},
                                       expires_after=timedelta(
                                            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
                                        ))
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}