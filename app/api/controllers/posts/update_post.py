from fastapi import status
from sqlalchemy.orm import Session

from ....db_services import update_post as update_post_db
from ....schemas import (
    ErrorResponse,
    Post as PostSchema,
    PostUpdate,
    UpdatePostResponse,
)


async def update_post(
    db: Session, post_id: int, post_data: PostUpdate, user_id: int
) -> UpdatePostResponse | ErrorResponse:
    try:
        post = await update_post_db(db, post_id, post_data, user_id)
        post_data = PostSchema(id=post.id, text=post.text, owner_id=post.owner_id)
        return UpdatePostResponse(
            status="SUCCESS",
            data=post_data,
            detail=f"Post {post.id} Updated Successfully!",
        )
    except Exception as e:
        db.rollback()
        print(f"Error Updating Post: {e}")
        return ErrorResponse(
            detail=str(e), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
