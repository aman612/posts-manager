from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreatedResponse(BaseModel):
    data: dict
    message: str
    status: str


class UserLoginResponse(BaseModel):
    data: dict
    status: str
