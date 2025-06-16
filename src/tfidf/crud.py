import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC
from pathlib import Path

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