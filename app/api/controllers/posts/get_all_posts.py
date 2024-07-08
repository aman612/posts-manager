from fastapi import status
from sqlalchemy.orm import Session

from ....db_services import read_posts
from ....schemas import (
    GetAllPostsResponse,
    ErrorResponse,
    Post as PostSchema,
)


async def get_all_posts(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> GetAllPostsResponse | ErrorResponse:
    try:
        posts = await read_posts(db=db, skip=skip, limit=limit, user_id=user_id)
        post_data = [
            PostSchema(id=post.id, text=post.text, owner_id=post.owner_id)
            for post in posts
        ]
        return GetAllPostsResponse(status="SUCCESS", data=post_data)
    except Exception as e:
        print(f"Error While Getting All Posts: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
