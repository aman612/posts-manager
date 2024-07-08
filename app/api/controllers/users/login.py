from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....db_services import get_user_by_email
from ....schemas import (
    ErrorResponse,
    UserCreate,
    UserLoginResponse,
)
from ....utils import create_access_token, verify_password


async def login(db: Session, user: UserCreate) -> UserLoginResponse | ErrorResponse:
    try:
        db_user = await get_user_by_email(db, email=user.email)

        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        token = create_access_token(data={"sub": db_user.email})
        return UserLoginResponse(data={"token": token}, status="SUCCESS")
    except Exception as e:
        print(f"Error While Login User: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
