from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from tfidf.schemas import MetricsOut


async def get_metrics_tfidf(session: AsyncSession) -> MetricsOut:
    result = None
    if not result:
        result = MetricsOut(
            files_processed=0,
            min_time_processed=0,
            avg_time_processed=0,
            max_time_processed=0,
            latest_file_processed_timestamp=datetime.min,
        )

    return result
