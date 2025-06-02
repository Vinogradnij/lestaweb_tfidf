from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tfidf.models import Records
from tfidf.schemas import RecordsOut


async def get_metrics_tfidf(session: AsyncSession) -> RecordsOut:
    stmt = select(Records)
    result = await session.scalar(stmt)
    if not result:
        result = RecordsOut(
            files_processed=0,
            min_time_processed=0,
            avg_time_processed=0,
            max_time_processed=0,
            latest_file_processed_timestamp=datetime.min,
        )
    else:
        result = RecordsOut(**Records.__dict__)
    return result
