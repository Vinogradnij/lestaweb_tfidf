from fastapi import APIRouter,HTTPException, status

from dependencies import session_dep, form_data_dep
from users.schemas import UserBase, UserPassword, Token
from users.crud import create_user, auth_user, get_user_by_username
from users.schemas import UserBase, UserPassword
from users.utils import create_access_token

router = APIRouter(
    tags=['Пользователи'],
)


@router.post(
    '/login',
    summary='Авторизация',
    response_model=Token
)
async def login(
        session: session_dep,
        form_data: form_data_dep,
):
    user = await auth_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    access_token = create_access_token(
        data={'sub': user.username}
    )
    return {'message': 'Вы успешно вошли в систему'}



@router.post(
    '/register',
    summary='Регистрация',
    response_model=UserBase,
)
async def register(
        user_in: UserPassword,
        session: session_dep,
):
    check_user = await get_user_by_username(session=session, username=user_in.username)
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
