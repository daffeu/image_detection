from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.utils import OAuth2PasswordBearerWithCookie

from core.hashing import Hasher
from core.security import create_access_token
from db.repository.auth import get_user
from db.session import get_db
from schemas.tokens import Token
from jose import jwt, JWTError


router = APIRouter()


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, "super-secret-keys", algorithms=["HS256"]
        )
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user