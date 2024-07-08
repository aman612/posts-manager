from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....db_services import (
    read_post_by_id,
    delete_post_by_id,
)
from ....schemas import (
    DeletePostResponse,
    ErrorResponse,
)


async def delete_post(
    db: Session, post_id: int, user_id: int
) -> DeletePostResponse | ErrorResponse:
    try:
        post = await read_post_by_id(db=db, post_id=post_id, user_id=user_id)
        if post is None or post.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Post not found")

        await delete_post_by_id(db=db, post_id=post.id, user_id=user_id)
        return DeletePostResponse(status="SUCCESS", detail="Post Deleted Successfully!")
    except Exception as e:
        print(f"Error Deleting Post: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
