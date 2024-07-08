from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ...config import get_db
from ..controllers.posts import (
    add_post,
    delete_post,
    get_all_posts,
    get_post_by_id,
    update_post,
)
from ...db_services import get_user_by_email
from ...models import User as UserModel
from ...schemas import (
    DeletePostResponse,
    ErrorResponse,
    GetAllPostsResponse,
    GetPostByIdResponse,
    PostCreate,
    PostCreatedResponse,
    PostUpdate,
    UpdatePostResponse,
)
from ...utils import verify_token


router = APIRouter()

cache = TTLCache(maxsize=100, ttl=300)


def get_auth_token(authorization: str) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Unauthorized")

    token = authorization.split(" ")[1]
    return token


async def get_current_user(
    token: str = Depends(verify_token), db: Session = Depends(get_db)
) -> UserModel:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=403, detail="Invalid authentication credentials"
        )
    user = await get_user_by_email(db, email=payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/add-post", response_model=PostCreatedResponse | ErrorResponse)
async def add_post_handler(
    post: PostCreate, authorization: str = Header(None), db: Session = Depends(get_db)
) -> PostCreatedResponse | ErrorResponse:

    token = get_auth_token(authorization)
    user = await get_current_user(token, db)
    if len(post.text.encode("utf-8")) > 1 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload too large. It should be 1MB.")

    return await add_post(db=db, post=post, user_id=user.id)


@router.delete(
    "/delete-post/{post_id}", response_model=DeletePostResponse | ErrorResponse
)
async def delete_post_handler(
    post_id: int, authorization: str = Header(None), db: Session = Depends(get_db)
) -> None:

    token = get_auth_token(authorization)
    user = await get_current_user(token, db)

    return await delete_post(db=db, post_id=post_id, user_id=user.id)


@router.get("/get-all-posts", response_model=GetAllPostsResponse | ErrorResponse)
async def get_all_posts_handler(
    skip: int = 0,
    limit: int = 10,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> GetAllPostsResponse | ErrorResponse:

    token = get_auth_token(authorization)
    user = await get_current_user(token, db)

    posts = await get_all_posts(db=db, skip=skip, limit=limit, user_id=user.id)
    cache[user.id] = posts

    return posts


@router.get(
    "/get-post-by-id/{post_id}", response_model=GetPostByIdResponse | ErrorResponse
)
async def get_post_by_id_handler(
    post_id: int, authorization: str = Header(None), db: Session = Depends(get_db)
) -> GetAllPostsResponse | ErrorResponse:

    token = get_auth_token(authorization)
    user = await get_current_user(token, db)

    return await get_post_by_id(db, post_id, user_id=user.id)


@router.put("/update-post/{post_id}", response_model=UpdatePostResponse | ErrorResponse)
async def update_post_handler(
    post_id: int,
    post_data: PostUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> UpdatePostResponse | ErrorResponse:

    token = get_auth_token(authorization)
    user = await get_current_user(token, db)

    return await update_post(
        db=db, post_id=post_id, post_data=post_data, user_id=user.id
    )
