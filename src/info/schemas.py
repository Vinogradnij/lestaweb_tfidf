from datetime import datetime

from pydantic import BaseModel


class MetricsOut(BaseModel):
    files_processed: int
    min_time_processed: float
    avg_time_processed: float
    max_time_processed: float
    latest_file_processed_timestamp: datetime