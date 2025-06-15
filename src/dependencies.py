from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler

session_dep = Annotated[AsyncSession, Depends(db_handler.session_dep)]

def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return token

token_dep = Annotated[str, Depends(get_token)]