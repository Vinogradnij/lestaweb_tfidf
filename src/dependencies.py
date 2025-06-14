from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler
from users.schemas import UserBase

session_dep = Annotated[AsyncSession, Depends(db_handler.session_dep)]
