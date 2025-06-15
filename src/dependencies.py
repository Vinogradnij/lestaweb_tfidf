from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler
from users.utils import get_token

session_dep = Annotated[AsyncSession, Depends(db_handler.session_dep)]

token_dep = Annotated[str, Depends(get_token)]