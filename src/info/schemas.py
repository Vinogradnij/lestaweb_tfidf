from pydantic import BaseModel


class MetricsOut(BaseModel):
    collection_processed: int
    min_time_processed: float
    avg_time_processed: float
    max_time_processed: float
    all_time_processed: float
    latest_file_processed_timestamp: float

    files_huffman: int
    min_time_huffman: float
    avg_time_huffman: float
    max_time_huffman: float
    all_time_huffman: float
    latest_huffman: float