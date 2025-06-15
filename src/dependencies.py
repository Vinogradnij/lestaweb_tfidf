from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler

session_dep = Annotated[AsyncSession, Depends(db_handler.session_dep)]

form_data_dep = Annotated[OAuth2PasswordRequestForm, Depends()]

auth_dep = Annotated[UserBase, Depends()]