from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from jose.exceptions import JWTError
from jose import jwt

from users.models import User
from users.schemas import UserPassword, UserInDb
from users.utils import hash_password, verify_password
from dependencies import token_dep
from users.schemas import UserBase, TokenData
from config import settings


async def create_user(session: AsyncSession, user_in: UserPassword) -> UserInDb:
    hashed_pass = hash_password(user_in.password)
    user = UserInDb(username=user_in.username, hashed_password=hashed_pass)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_current_user(session: AsyncSession, token: token_dep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        auth_data = settings.auth_data
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def auth_user(session: AsyncSession, username: str, password: str) -> UserBase | bool:
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return UserBase(username=user.username)
