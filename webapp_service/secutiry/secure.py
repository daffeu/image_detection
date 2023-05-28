from datetime import datetime, timedelta

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from secutiry.utils import OAuth2PasswordBearerWithCookie
from jose import jwt, JWTError
from passlib.context import CryptContext

from db_config.mongo_config import create_db_collections
from models.request.tokens import TokenData
from repository.user import UserRepository

SECRET_KEY = "tbWivbkVxfsuTxCP8A+Xg67LcmjXXl/sszHXwH+TX9w="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


def get_password_hash(password):
    return crypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


def authenticate(password, account_password):
    try:
        password_check = verify_password(password, account_password)
        return password_check
    except Exception as e:
        return False


def create_access_token(data: dict, expires_after: timedelta):
    plain_text = data.copy()
    expire = datetime.utcnow() + expires_after
    plain_text.update({"exp": expire})
    encoded_jwt = jwt.encode(plain_text, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),
                     db=Depends(create_db_collections)):

    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"}
    # )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except (JWTError, AttributeError):
        return None
    repo = UserRepository(db)
    user = repo.get_user(token_data.username)
    if user is None:
        return None
    return user
