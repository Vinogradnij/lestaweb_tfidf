from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    login: str


class UserIn(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class UserOut(UserBase):
    pass
