from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from jose.exceptions import JWTError
from jose import jwt

from database import db_handler
from users.models import User
from users.schemas import UserPassword, UserInDb
from users.utils import hash_password, verify_password
from dependencies import token_dep
from users.schemas import UserBase, TokenData
from config import settings


async def create_user(session: AsyncSession, user_in: UserPassword) -> UserInDb:
    hashed_pass = hash_password(user_in.password)
    user = User(username=user_in.username, password=hashed_pass)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserInDb(username=user.username, hashed_password=user.password, id=user.id)

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_current_user(token: token_dep) -> UserInDb:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
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
    async with db_handler.session_factory() as session:
        user = await get_user_by_username(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserInDb(username=user.username, hashed_password=user.password, id=user.id)

async def auth_user(session: AsyncSession, username: str, password: str) -> UserBase | None:
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return UserBase(username=user.username)

async def verify_id(session: AsyncSession, user_id: int, current_user: UserBase) -> None:
    request_user = await get_user_by_username(session=session, username=current_user.username)
    if request_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not allowed changing')

async def change_password(session: AsyncSession, password: str, user_id: int, current_user: UserBase) -> UserInDb:
    await verify_id(session=session, user_id=user_id, current_user=current_user)
    user = await get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    hashed_pass = hash_password(password)
    user.password = hashed_pass
    await session.commit()
    await session.refresh(user)
    return UserInDb(username=user.username, hashed_password=hashed_pass, id=user.id)

async def delete_user_by_id(session: AsyncSession, user_id: int, current_user: UserBase):
    await verify_id(session=session, user_id=user_id, current_user=current_user)
    user = await get_user_by_id(session=session, user_id=user_id)
    await session.delete(user)
    await session.commit()