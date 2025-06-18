from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Metrics(Base):
    id: Mapped[int] = mapped_column(primary_key=True, default=1)

    files_processed: Mapped[int]
    min_time_processed: Mapped[float]
    avg_time_processed: Mapped[float]
    max_time_processed: Mapped[float]
    all_time_processed: Mapped[float]
    latest_file_processed_timestamp: Mapped[float]

    files_huffman: Mapped[int]
    min_time_huffman: Mapped[float]
    avg_time_huffman: Mapped[float]
    max_time_huffman: Mapped[float]
    all_time_huffman: Mapped[float]
    latest_huffman: Mapped[float]