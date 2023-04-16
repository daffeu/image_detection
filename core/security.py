from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=60
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, "super-secret-keys", algorithm="HS256"
    )
    return encoded_jwt
