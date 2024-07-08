from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....db_services import create_user, get_user_by_email
from ....schemas import UserCreate, UserCreatedResponse, ErrorResponse
from ....utils import get_password_hash, create_access_token


async def signup(db: Session, user: UserCreate) -> UserCreatedResponse | ErrorResponse:
    try:
        existed_user = await get_user_by_email(db, email=user.email)
        if existed_user:
            raise HTTPException(status_code=400, detail="Email Already Exists")

        hashed_password = get_password_hash(user.password)
        user.password = hashed_password

        new_user = await create_user(db=db, user=user)

        token = create_access_token(data={"sub": new_user.email})

        return UserCreatedResponse(
            data={"token": token},
            message=f"User {new_user.email} Created Successfully!",
            status="SUCCESS",
        )
    except Exception as e:
        print(f"Error while creating user: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
