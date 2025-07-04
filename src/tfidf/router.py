from typing import Annotated

from fastapi import UploadFile, APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse

from dependencies import session_dep
from tfidf.schemas import DocumentOut, StatisticCollectionOut, StatisticWordOut, CollectionOut, DocumentOnlyIdOut
from tfidf.crud import save_files, get_files, get_files_text, delete_file, get_collections_with_files, \
    get_collection_with_files, add_document_to_collection, pop_document_from_collection, compute_statistics, \
    get_statistic_from_document, get_statistic_from_collection, encode_text_by_huffman
from users.crud import get_current_user
from users.schemas import UserInDb

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
    summary='Загрузка файлов',
    response_model=StatisticCollectionOut,
)
async def upload_files(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        files: list[UploadFile]
):
    for file in files:
        if file.content_type != 'text/plain':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    collection_id = await save_files(session=session, current_user=current_user, files=files)

    results = await compute_statistics(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )

    return results


@router.get(
    '/documents',
    summary='Получить список документов пользователя',
    response_model=list[DocumentOut]
)
async def get_documents(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    documents = await get_files(session=session, current_user=current_user)
    if documents is None:
        return {'message': 'У пользователя ещё нет файлов'}
    return documents


@router.get(
    '/documents/{document_id}',
    summary='Получить содержимое документа'
)
async def get_document(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        document_id: int,
):
    document = await get_files_text(session=session, current_user=current_user, document_id=document_id)
    return document


@router.get(
    '/documents/{document_id}/statistics',
    summary='Получить статистику по данному документу',
    response_model=list[StatisticWordOut],
)
async def get_document_statistics(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        document_id: int,
):
    result = await get_statistic_from_document(
        session=session,
        current_user=current_user,
        document_id=document_id
    )
    return result


@router.get(
    '/documents/{document_id}/huffman',
    summary='Получить содержимое документа, закодированное Кодом Хаффмана',
)
async def get_huffman(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        document_id: int,
):
    result = await encode_text_by_huffman(session=session, current_user=current_user, document_id=document_id)
    return result

@router.delete(
    '/documents/{document_id}',
    summary='Удалить документ'
)
async def delete_document(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        document_id: int,
):
    await delete_file(session=session, current_user=current_user, document_id=document_id)
    return {'message': 'Файл успешно удален'}


@router.get(
    '/collections',
    summary='Получить список коллекций и список входящих в них документов',
    response_model=list[CollectionOut]
)
async def get_collections(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    collections = await get_collections_with_files(session=session, current_user=current_user)
    if not collections:
        return {'message': 'У пользователя нет коллекций'}
    return collections


@router.get(
    '/collections/{collection_id}',
    summary='Получить список входящих в коллекцию id документов',
    response_model=list[DocumentOnlyIdOut],
)
async def get_collection(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        collection_id: int,
):
    collection = await get_collection_with_files(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )
    return collection


@router.get(
    '/collections/{collection_id}/statistics',
    summary='Получить статистику по коллекции',
    response_model=list[StatisticWordOut]
)
async def get_collection_statistics(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        collection_id: int
):
    result = await get_statistic_from_collection(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )

    return result


@router.post(
    '/collections/{collection_id}/{document_id}',
    summary='Добавить документ в коллекцию'
)
async def add_document(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        collection_id: int,
        document_id: int,
):
    await add_document_to_collection(
        session=session,
        current_user=current_user,
        document_id=document_id,
        collection_id=collection_id
    )

    return {'message': 'Документ добавлен в коллекцию'}


@router.delete(
    '/collections/{collection_id}/{document_id}',
    summary='Удалить документ из коллекции'
)
async def delete_document_from_collection(
        session: session_dep,
        current_user: Annotated[UserInDb, Depends(get_current_user)],
        collection_id: int,
        document_id: int,
):
    await pop_document_from_collection(
        session=session,
        current_user=current_user,
        document_id=document_id,
        collection_id=collection_id
    )

    return {'message': 'Документ удалён из коллекции'}
