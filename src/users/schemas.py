from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class UserOut(UserBase):
    pass
