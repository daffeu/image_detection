from core.hashing import Hasher
from db.models.users import User
from schemas.auth import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
