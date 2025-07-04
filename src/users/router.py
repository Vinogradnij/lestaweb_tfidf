from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends

from dependencies import session_dep
from users.schemas import UserBase, UserPassword, PasswordBase
from users.crud import create_user, auth_user, get_user_by_username, get_current_user, change_password, \
    delete_user_by_id
from users.utils import create_access_token

router = APIRouter(
    tags=['Пользователи'],
)


@router.post(
    '/login',
    summary='Авторизация',
)
async def login(
        session: session_dep,
        user_in: UserPassword,
        response: Response
):
    user = await auth_user(session=session, username=user_in.username, password=user_in.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token = create_access_token(data={'sub': user.username})
    response.set_cookie(key='access_token', value=access_token)
    return {'message': 'Вы успешно вошли в систему'}


@router.post(
    '/register',
    summary='Регистрация',
)
async def register(
        user_in: UserPassword,
        session: session_dep,
):
    check_user = await get_user_by_username(session=session, username=user_in.username)
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    user = await create_user(session=session, user_in=user_in)
    return {'message': f'Пользователь {user.username} успешно зарегистрирован'}


@router.get(
    '/logout',
    summary='Логаут',
)
async def logout(
        current_user: Annotated[UserBase, Depends(get_current_user)],
        response: Response,
):
    response.delete_cookie(key='access_token')
    return {'message': f'Пользователь {current_user.username} успешно вышел из системы'}


@router.patch(
    '/user/{user_id}',
    summary='Изменение пароля',
)
async def edit_pass(
        session: session_dep,
        current_user: Annotated[UserBase, Depends(get_current_user)],
        password_in: PasswordBase,
        user_id: int,
):
    user = await change_password(
        session=session, password=password_in.password, user_id=user_id, current_user=current_user
    )
    return {'message': f'Пароль пользователя {user.username} успешно изменён'}


@router.delete(
    '/user/{user_id}',
    summary='Удаление пользователя',
)
async def delete_user(
        session: session_dep,
        current_user: Annotated[UserBase, Depends(get_current_user)],
        user_id: int,
        response: Response,
):
    await delete_user_by_id(session=session, user_id=user_id, current_user=current_user)
    response.delete_cookie(key='access_token')
    return {'message': f'Пользователь {current_user.username} успешно удален'}

