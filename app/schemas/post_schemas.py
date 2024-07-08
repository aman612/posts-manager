from pydantic import BaseModel, constr


class PostBase(BaseModel):
    text: constr(max_length=1024)  # type: ignore


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    text: constr(max_length=1024)  # type: ignore


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        # orm_mode = True
        model_config = {"from_attributes": True}


class PostCreatedResponse(BaseModel):
    message: str
    status: int


class GetAllPostsResponse(BaseModel):
    status: str
    data: list[Post]


class GetPostByIdResponse(BaseModel):
    status: str
    data: Post


class DeletePostResponse(BaseModel):
    status: str
    detail: str


class UpdatePostResponse(BaseModel):
    status: str
    data: Post
    detail: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: int = None
    additional_info: dict = None
