import aiofiles
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, and_
from datetime import datetime, UTC
from pathlib import Path
from collections import deque

from tfidf.schemas import DocumentOut
from users.schemas import UserInDb
from tfidf.models import Document, Collection, Collection_Document
from definitions import ROOT_SRC


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
        print(ROOT_SRC)
        Path(f'{ROOT_SRC}/files/{username}/{date}').mkdir(parents=True, exist_ok=True  )

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


async def get_files(session: AsyncSession, current_user: UserInDb) -> list[DocumentOut] | None:
    documents = await session.execute(Select(Document).where(Document.user_id == current_user.id))
    documents = documents.scalars().all()
    if documents is None:
        return None
    results = [DocumentOut(id=doc.id, title=doc.title) for doc in documents.scalars().all()]
    return results


async def get_file_by_id(session: AsyncSession, current_user: UserInDb, document_id: int) -> Document:
    document = await session.execute(
        Select(Document).where(and_(Document.user_id == current_user.id, Document.id == document_id))
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
