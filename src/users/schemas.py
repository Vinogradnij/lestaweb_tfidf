from pydantic import BaseModel


class PasswordBase(BaseModel):
    password: str


class UserBase(BaseModel):
    username: str


class UserInDb(UserBase):
    hashed_password: str
    id: int


class UserPassword(PasswordBase, UserBase):
    pass


class TokenData(BaseModel):
    username: str | None = None
