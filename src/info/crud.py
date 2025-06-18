from datetime import datetime, UTC, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from info.schemas import MetricsOut
from info.models import Metrics


async def add_metrics(
        session: AsyncSession,
        number_of_files: int,
        duration: float,
        for_huffman: bool = False,
):
    metrics = await session.get(Metrics, 1)

    if not for_huffman:
        metrics.files_processed += number_of_files
        metrics.min_time_processed = metrics.min_time_processed \
            if metrics.min_time_processed < duration else duration
        metrics.all_time_processed += duration
        metrics.avg_time_processed = metrics.avg_time_processed \
            if metrics.files_processed == 0 else metrics.all_time_processed / metrics.files_processed
        metrics.max_time_processed = metrics.max_time_processed \
            if metrics.max_time_processed > duration else duration
        metrics.latest_file_processed_timestamp=(datetime.now(UTC) - timedelta(seconds=duration)).timestamp()
    else:
        metrics.files_huffman += number_of_files
        metrics.min_time_huffman = metrics.min_time_huffman \
            if metrics.min_time_huffman < duration else duration
        metrics.all_time_huffman += duration
        metrics.avg_time_huffman = metrics.avg_time_huffman \
            if metrics.files_huffman == 0 else metrics.all_time_huffman / metrics.files_huffman
        metrics.max_time_huffman = metrics.max_time_huffman \
            if metrics.max_time_huffman > duration else duration
        metrics.latest_huffman=duration
    await session.commit()
