from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import UserCreate
from users.utils import hash_password


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    hashed_pass = hash_password(user_in.password)
    user = User(login=user_in.login, password=hashed_pass)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user