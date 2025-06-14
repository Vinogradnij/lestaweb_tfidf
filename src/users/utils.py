from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import datetime, timezone, timedelta

from users.crud import get_user_by_username
from users.schemas import UserBase
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def check_user_in_db(session: AsyncSession, username: str) -> bool:
    user_in_db = await get_user_by_username(session=session, username=username)
    return True if user_in_db else False

async def auth_user(session: AsyncSession, username: str, password: str) -> UserBase | bool:
    user = await get_user_by_username(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return UserBase(username=user.username)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({'exp': expire})
    auth_data = settings.auth_data
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt