from fastapi import APIRouter

from users.dependencies import session_dep
from users.schemas import UserCreate, UserLogout
from users.crud import create_user

router = APIRouter(
    tags=['Пользователи'],
)


@router.post(
    '/login',
    summary='Авторизация',
)
async def login(
        session: session_dep,
):
    pass


@router.post(
    '/register',
    summary='Регистрация',
    response_model=UserLogout,
)
async def register(
        user_in: UserCreate,
        session: session_dep,
):
    user = await create_user(session=session, user_in=user_in)
    return user


@router.get(
    '/logout',
    summary='Логаут',
)
async def logout(
        session: session_dep,
):
    pass


@router.patch(
    '/user/{user_id}',
    summary='Изменение пароля',
)
async def edit_pass(
        session: session_dep,
):
    pass


@router.delete(
    '/user/{user_id}',
    summary='Удаление пользователя',
)
async def delete_user(
        session: session_dep,
):
    pass
