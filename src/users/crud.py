from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from users.models import User
from users.schemas import UserPassword, UserInDb
from users.utils import hash_password


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
