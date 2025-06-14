from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserInDb(UserBase):
    hashed_password: str


class UserPassword(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
