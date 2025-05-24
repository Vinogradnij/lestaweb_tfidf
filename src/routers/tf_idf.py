from fastapi import UploadFile, APIRouter
from fastapi.responses import HTMLResponse

from utils import compute_tfidf

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
async def upload_files(files: list[UploadFile]):
    results = compute_tfidf(files)
    return results