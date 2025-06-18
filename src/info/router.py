from fastapi import APIRouter, Request

from dependencies import session_dep
from info.schemas import MetricsOut
from info.crud import get_metrics_crud

router = APIRouter(
    tags=['Служебная информация'],
)

@router.get(
    '/metrics',
    summary='Метрики приложения',
    response_model=MetricsOut
)
async def get_metrics(
        session: session_dep,
):
    metrics = await get_metrics_crud(session=session)
    return metrics


@router.get(
    '/status',
    summary='Статус приложения',
)
async def get_status():
    return {'status': 'OK'}

@router.get(
    '/version',
    summary='Версия приложения',
)
async def get_version(request: Request):
    version = request.app.version
    return {'version': version}
