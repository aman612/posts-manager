from sqlalchemy.orm import Session

from ..models import User as UserModel
from ..schemas import UserCreate


async def create_user(db: Session, user: UserCreate) -> UserModel:
    db_user = UserModel(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user_by_email(db: Session, email: str) -> UserModel | None:
    user = db.query(UserModel).filter(UserModel.email == email).first()
    return user
