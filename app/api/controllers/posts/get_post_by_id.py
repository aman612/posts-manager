from fastapi import status
from sqlalchemy.orm import Session

from ....db_services import read_post_by_id
from ....schemas import (
    ErrorResponse,
    GetPostByIdResponse,
    Post as PostSchema,
)


async def get_post_by_id(
    db: Session, post_id: int, user_id: int
) -> GetPostByIdResponse | ErrorResponse:
    try:
        post = await read_post_by_id(db=db, post_id=post_id, user_id=user_id)
        post_data = PostSchema(id=post.id, text=post.text, owner_id=post.owner_id)
        return GetPostByIdResponse(status="SUCCESS", data=post_data)
    except Exception as e:
        print(f"Error While Getting Post: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
