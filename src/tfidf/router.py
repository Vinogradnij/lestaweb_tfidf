from typing import Annotated

from fastapi import UploadFile, APIRouter, HTTPException, status, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler
from tfidf.files_handler import compute_tfidf
from tfidf.schemas import OutputResults, MetricsOut
from tfidf.service import get_metrics_tfidf

router = APIRouter(
    tags=['Анализ tf_idf'],
)


@router.get(
    '/',
    summary='Главная страница',
    response_class=HTMLResponse,
)
async def home():
    content = """
    <body>
    <form action="/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
        """
    return content


@router.post(
    '/',
    summary='Загрузка файла',
)
async def upload_files(files: list[UploadFile]) -> OutputResults:
    for file in files:
        if file.content_type != 'text/plain':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    results = compute_tfidf(files)
    return OutputResults(results=results)


@router.get(
    '/metrics',
    summary='Метрики приложения',
    tags=['Служебная информация'],
    response_model=MetricsOut
)
async def get_metrics(
        session: Annotated[AsyncSession, Depends(db_handler.session_dep)],
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
