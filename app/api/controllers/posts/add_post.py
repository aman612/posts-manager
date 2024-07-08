from fastapi import status
from sqlalchemy.orm import Session

from ....db_services import create_post
from ....schemas import (
    ErrorResponse,
    PostCreate,
    PostCreatedResponse,
)


async def add_post(
    db: Session, post: PostCreate, user_id: int
) -> PostCreatedResponse | ErrorResponse:
    try:
        post = await create_post(db=db, post=post, user_id=user_id)
        return PostCreatedResponse(
            status=status.HTTP_201_CREATED,
            message=f"Post {post.id} created successfully!",
        )
    except Exception as e:
        db.rollback()
        print(f"Error Creating Post: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
