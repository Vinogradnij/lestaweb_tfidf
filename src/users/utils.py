from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from users.crud import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def check_user_in_db(session: AsyncSession, username: str) -> bool:
    user_in_db = await get_user_by_username(session=session, username=username)
    return True if user_in_db else False
