from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(UserBase):
    password: str


class UserLogout(UserBase):
    pass
