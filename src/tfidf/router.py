from typing import Annotated

from fastapi import UploadFile, APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_handler
from tfidf.files_handler import compute_tfidf
from tfidf.schemas import OutputResults, RecordsOut
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
    response_model=RecordsOut
)
async def get_metrics(
        session: Annotated[AsyncSession, Depends(db_handler.session_dep)],
):
    metrics = await get_metrics_tfidf(session=session)
    return metrics
