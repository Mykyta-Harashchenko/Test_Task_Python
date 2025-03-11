from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserSignin(BaseModel):
    email: str
    password: str


class UserSignup(BaseModel):
    email: EmailStr
    username: str
    password: str
