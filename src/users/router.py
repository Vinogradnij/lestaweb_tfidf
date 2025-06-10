from fastapi import APIRouter

router = APIRouter(
    tags=['Пользователи'],
)


@router.post(
    '/login',
    summary='Авторизация',
)
async def login():
    pass


@router.post(
    '/register',
    summary='Регистрация',
)
async def register():
    pass


@router.get(
    '/logout',
    summary='Логаут',
)
async def logout():
    pass


@router.patch(
    '/user/{user_id}',
    summary='Изменение пароля',
)
async def edit_pass():
    pass


@router.delete(
    '/user/{user_id}',
    summary='Удаление пользователя',
)
async def delete_user():
    pass
