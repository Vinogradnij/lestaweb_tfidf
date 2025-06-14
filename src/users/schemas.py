from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserInDb(UserBase):
    hashed_password: str

class UserPassword(UserBase):
    password: str
