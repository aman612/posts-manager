from fastapi import APIRouter

from . import posts, users

base_router = APIRouter()

base_router.include_router(
    posts.router, tags=["posts"], prefix="/post"
) 
base_router.include_router(users.router, tags=["users"], prefix="/user")
