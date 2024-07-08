from sqlalchemy.orm import Session

from ..models import Post as PostModel
from ..schemas import (
    PostCreate,
    PostUpdate,
)


async def create_post(db: Session, post: PostCreate, user_id: int) -> PostModel:

    db_post = PostModel(**post.model_dump(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


async def read_posts(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> list[PostModel]:

    posts = (
        db.query(PostModel)
        .filter(PostModel.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


async def read_post_by_id(db: Session, post_id: int, user_id: int) -> PostModel:

    post = (
        db.query(PostModel)
        .filter(PostModel.owner_id == user_id)
        .filter(PostModel.id == post_id)
        .one_or_none()
    )
    return post


async def delete_post_by_id(db: Session, post_id: int, user_id: int) -> None:
    post = await read_post_by_id(db, post_id, user_id)
    db.delete(post)
    db.commit()


async def update_post(
    db: Session, post_id: int, post_data: PostUpdate, user_id: int
) -> PostModel:
    post = await read_post_by_id(db, post_id, user_id)
    for field, value in post_data.dict().items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post
