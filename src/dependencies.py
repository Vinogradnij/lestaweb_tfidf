from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler
from users.schemas import UserBase

session_dep = Annotated[AsyncSession, Depends(db_handler.session_dep)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
token_dep = Annotated[str, Depends(oauth2_scheme)]

form_data_dep = Annotated[OAuth2PasswordRequestForm, Depends()]
