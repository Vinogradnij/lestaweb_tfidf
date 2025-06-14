from fastapi import APIRouter,HTTPException, status

from dependencies import session_dep
from users.schemas import UserCreate, UserLogout
from users.crud import create_user
from users.utils import check_user_in_db

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
    check_user = check_user_in_db(session=session, username=user_in.username)
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
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
