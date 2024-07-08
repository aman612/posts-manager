from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...config import get_db
from ...api.controllers.users import login, signup
from ...schemas import (
    ErrorResponse,
    UserCreate,
    UserCreatedResponse,
    UserLoginResponse,
)

router = APIRouter()


@router.post("/signup", response_model=UserCreatedResponse | ErrorResponse)
async def signup_handler(
    user: UserCreate, db: Session = Depends(get_db)
) -> UserCreatedResponse | ErrorResponse:
    return await signup(db, user)


@router.post("/login")
async def login_handler(
    user: UserCreate, db: Session = Depends(get_db)
) -> UserLoginResponse | ErrorResponse:
    return await login(db, user)
