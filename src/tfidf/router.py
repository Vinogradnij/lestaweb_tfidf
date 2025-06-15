from fastapi import UploadFile, APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse

from tfidf.files_handler import compute_tfidf
from tfidf.schemas import OutputResults

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
    '/documents',
    summary='Получить список документов пользователя'
)
async def get_documents():
    pass


@router.get(
    '/documents/{document_id}',
    summary='Получить содержимое документа'
)
async def get_document():
    pass


@router.get(
    '/documents/{document_id}/statistics',
    summary='Получить статистику по данному документу'
)
async def get_document_statistics():
    pass


@router.delete(
    '/documents/{document_id}',
    summary='Удалить документ'
)
async def delete_document():
    pass


@router.get(
    '/collections',
    summary='Получить список коллекций и список входящих в них документов'
)
async def get_collections():
    pass


@router.get(
    '/collections/{collection_id}',
    summary='Получить список входящих в коллекцию id документов'
)
async def get_collection():
    pass


@router.get(
    '/collections/{collection_id}/statistics',
    summary='Получить статистику по коллекции'
)
async def get_collection_statistics():
    pass


@router.post(
    '/collections/{collection_id}/{document_id}',
    summary='Добавить документ в коллекцию'
)
async def add_document():
    pass


@router.delete(
    '/collections/{collection_id}/{document_id}',
    summary='Удалить документ из коллекции'
)
async def add_document():
    pass
