import time

import aiofiles
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, UTC
from pathlib import Path
from collections import deque

from sqlalchemy.orm import selectinload

from tfidf.handler import analyze_collection
from tfidf.schemas import DocumentOut, CollectionOut, DocumentOnlyIdOut, DocumentInDb, StatisticCollectionOut, \
    StatisticWordOut
from users.schemas import UserInDb
from tfidf.models import Document, Collection, Collection_Document, Statistic
from definitions import ROOT
from huffman.service import get_frequency, encode
from huffman.tree import HuffmanTree
from info.crud import add_metrics


async def save_files(session: AsyncSession, current_user: UserInDb, files: list[UploadFile]):
    user_collection = Collection(user_id=current_user.id)
    session.add(user_collection)
    await session.commit()
    await session.refresh(user_collection)

    for file in files:
        username = current_user.username
        filename = file.filename
        date = datetime.now(UTC).strftime('%Y-%m-%d_%H:%M:%S')
        path = f'src/files/{username}/{date}/{filename}'
        Path(f'{ROOT}/src/files/{username}/{date}').mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(path, 'wb') as local_file:
            while chunks := await file.read(1024):
                await local_file.write(chunks)

        document = Document(title=filename, path=path, user_id=current_user.id)
        session.add(document)
        await session.commit()
        await session.refresh(document)

        user_collection_document = Collection_Document(document_id=document.id, collection_id=user_collection.id)
        session.add(user_collection_document)

    await session.commit()

    return user_collection.id

async def get_files(session: AsyncSession, current_user: UserInDb) -> list[DocumentOut] | None:
    documents = await session.execute(select(Document).where(Document.user_id == current_user.id))
    documents = documents.scalars().all()
    if documents is None:
        return None
    results = [DocumentOut(id=doc.id, title=doc.title) for doc in documents]
    return results


async def get_file_by_id(session: AsyncSession, current_user: UserInDb, document_id: int) -> Document:
    document = await session.execute(
        select(Document).where(and_(Document.user_id == current_user.id, Document.id == document_id))
    )
    document = document.scalar_one_or_none()

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')

    return document


async def get_files_text(session: AsyncSession, current_user: UserInDb, document_id: int) -> str:
    document = await get_file_by_id(session=session, current_user=current_user, document_id=document_id)

    result = deque()

    async with aiofiles.open(document.path) as local_file:
        while chunks := await local_file.read(1024):
            result.append(chunks)

    return ''.join(result)


async def encode_text_by_huffman(session: AsyncSession, current_user: UserInDb, document_id: int) -> str:
    document = await get_file_by_id(session=session, current_user=current_user, document_id=document_id)

    start_time = time.perf_counter()

    frequency = await get_frequency(path=document.path)
    tree = HuffmanTree()
    encoding = tree.get_encoding(frequency=frequency)
    result = await encode(path=document.path, encoding=encoding)

    end_time = time.perf_counter()
    duration = round(end_time - start_time, 3)
    await add_metrics(session=session, number_of_files=1, duration=duration, for_huffman=True)

    return result


async def delete_file(session: AsyncSession, current_user: UserInDb, document_id: int) -> None:
    document = await get_file_by_id(session=session, current_user=current_user, document_id=document_id)

    await session.delete(document)
    await session.commit()

    Path(ROOT / Path(document.path)).unlink()


async def get_collection_by_id(
        session: AsyncSession,
        current_user: UserInDb,
        collection_id: int
) -> Collection:
    stmt = select(Collection).where(and_(Collection.user_id == current_user.id, Collection.id == collection_id))
    collection = await session.execute(stmt)
    collection = collection.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')

    return collection


async def get_collections_with_files(session: AsyncSession, current_user: UserInDb) -> list[CollectionOut] | None:
    stmt = (
        select(Collection)
        .where(Collection.user_id == current_user.id)
        .options(
            selectinload(Collection.collection_documents)
            .joinedload(Collection_Document.document)
        )
        .order_by(Collection.id)
    )
    collections = await session.scalars(stmt)
    if collections is None:
        return None
    result = deque()
    for collection in collections:
        documents = deque()
        for col_doc in collection.collection_documents:
            documents.append(DocumentOut(id=col_doc.document.id, title=col_doc.document.title))
        result.append(CollectionOut(id=collection.id, documents=documents))
    return list(result)


async def get_collection_with_files(
        session: AsyncSession, current_user: UserInDb, collection_id: int
) -> list[DocumentOnlyIdOut]:
    stmt = (
        select(Collection)
        .where(and_(Collection.user_id == current_user.id, Collection.id == collection_id))
        .options(
            selectinload(Collection.collection_documents)
            .joinedload(Collection_Document.document)
        )
        .order_by(Collection.id)
    )

    collection = await session.execute(stmt)
    collection = collection.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')

    result = deque()

    for col_doc in collection.collection_documents:
        result.append(DocumentOnlyIdOut(id=col_doc.document.id))

    return list(result)


async def add_document_to_collection(
        session: AsyncSession,
        current_user: UserInDb,
        document_id: int,
        collection_id: int
) -> None:
    document = await get_file_by_id(
        session=session,
        current_user=current_user,
        document_id=document_id
    )
    collection = await get_collection_by_id(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )

    stmt = (
        select(Collection_Document)
        .where(
            and_(
                Collection_Document.collection_id == collection.id,
                Collection_Document.document_id == document.id
            )
        )
    )

    col_doc = await session.execute(stmt)
    col_doc = col_doc.scalar_one_or_none()

    if col_doc is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Document exists in collection')

    col_doc = Collection_Document(collection_id=collection.id, document_id=document.id)
    session.add(col_doc)
    await session.commit()
    await compute_statistics(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )


async def pop_document_from_collection(
        session: AsyncSession,
        current_user: UserInDb,
        document_id: int,
        collection_id: int
):
    document = await get_file_by_id(
        session=session,
        current_user=current_user,
        document_id=document_id
    )
    collection = await get_collection_by_id(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )

    stmt = (
        select(Collection_Document)
        .where(
            and_(
                Collection_Document.collection_id == collection.id,
                Collection_Document.document_id == document.id
            )
        )
    )

    col_doc = await session.execute(stmt)
    col_doc = col_doc.scalar_one_or_none()

    if col_doc is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Document not exists in collection')

    await session.delete(col_doc)
    await session.commit()
    await compute_statistics(
        session=session,
        current_user=current_user,
        collection_id=collection_id
    )


async def compute_statistics(
        session: AsyncSession,
        current_user: UserInDb,
        collection_id: int
) -> StatisticCollectionOut:
    start_time = time.perf_counter()
    stmt = (
        select(Collection)
        .where(and_(Collection.user_id == current_user.id, Collection.id == collection_id))
        .options(
            selectinload(Collection.collection_documents)
            .joinedload(Collection_Document.document)
        )
        .order_by(Collection.id)
    )

    collection = await session.execute(stmt)
    collection = collection.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')

    documents: list[DocumentInDb] = []

    for col_doc in collection.collection_documents:
        documents.append(
            DocumentInDb(
                id=col_doc.document.id, title=col_doc.document.title, path=col_doc.document.path
            )
        )

    statistics = await analyze_collection(documents)
    statistics_out = deque()
    for document_statistic in statistics:
        for document_id, words in document_statistic.items():
            list_statistic_word_out = deque()
            for word in words:
                list_statistic_word_out.append(
                    StatisticWordOut(
                        word=word.name,
                        tf=word.tf,
                        idf=word.idf
                    )
                )
                stmt = insert(Statistic).values(
                    document_id=document_id,
                    collection_id=collection_id,
                    word=word.name,
                    tf=word.tf,
                    idf=word.idf
                ).on_conflict_do_update(
                    index_elements=['document_id', 'collection_id', 'word'],
                    set_={
                        'tf': word.tf,
                        'idf': word.idf,
                    }
                )
                await session.execute(stmt)

            statistics_out.append({document_id: list(list_statistic_word_out)})
    await session.commit()

    end_time = time.perf_counter()
    duration = round(end_time - start_time, 3)
    number_of_collection = await get_collections_count(session=session)
    await add_metrics(session=session, number_of_files=number_of_collection, duration=duration)
    return StatisticCollectionOut(collection=list(statistics_out))


async def get_statistic_from_document(
        session: AsyncSession,
        current_user: UserInDb,
        document_id: int
) -> list[StatisticWordOut]:
    stmt = (
        select(Document)
        .where(and_(Document.user_id == current_user.id, Document.id == document_id))
        .options(
            selectinload(Document.statistics)
        )
    )
    document = await session.execute(stmt)
    document = document.scalar_one_or_none()
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    result = deque()
    for statistic in document.statistics:
        result.append(StatisticWordOut(word=statistic.word, tf=statistic.tf, idf=statistic.idf))

    return list(result)


async def get_statistic_from_collection(
        session: AsyncSession,
        current_user: UserInDb,
        collection_id: int
) -> list[StatisticWordOut]:
    stmt = (
        select(Collection)
        .where(and_(Collection.user_id == current_user.id, Collection.id == collection_id))
        .options(
            selectinload(Collection.collection_documents)
            .joinedload(Collection_Document.document)
        )
        .order_by(Collection.id)
    )

    collection = await session.execute(stmt)
    collection = collection.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')

    documents: list[DocumentInDb] = []

    for col_doc in collection.collection_documents:
        documents.append(
            DocumentInDb(
                id=col_doc.document.id, title=col_doc.document.title, path=col_doc.document.path
            )
        )

    statistics = await analyze_collection(documents, merged_tf=True, collection_id=collection_id)
    statistics_out = deque()
    for document_statistic in statistics:
        for document_id, words in document_statistic.items():
            list_statistic_word_out = deque()
            for word in words:
                list_statistic_word_out.append(
                    StatisticWordOut(
                        word=word.name,
                        tf=word.tf,
                        idf=word.idf
                    )
                )
            statistics_out.extend(list_statistic_word_out)

    return list(statistics_out)


async def get_collections_count(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Collection))
    result = result.scalar_one()
    return result
