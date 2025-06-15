from fastapi import APIRouter, Request

from dependencies import session_dep
from info.schemas import MetricsOut
from info.service import get_metrics_tfidf

router = APIRouter(
    tags=['Анализ tf_idf'],
)

@router.get(
    '/metrics',
    summary='Метрики приложения',
    tags=['Служебная информация'],
    response_model=MetricsOut
)
async def get_metrics(
        session: session_dep,
):
    metrics = await get_metrics_tfidf(session=session)
    return metrics


@router.get(
    '/status',
    summary='Статус приложения',
    tags=['Служебная информация'],
)
async def get_status():
    return {'status': 'OK'}

@router.get(
    '/version',
    summary='Версия приложения',
    tags=['Служебная информация'],
)
async def get_version(request: Request):
    version = request.app.version
    return {'version': version}
