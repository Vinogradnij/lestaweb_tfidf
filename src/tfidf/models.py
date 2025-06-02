from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Records(Base):
    files_processed: Mapped[int]
    min_time_processed: Mapped[float]
    avg_time_processed: Mapped[float]
    max_time_processed: Mapped[float]
    latest_file_processed_timestamp = mapped_column(TIMESTAMP, nullable=False)
