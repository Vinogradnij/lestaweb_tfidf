from typing import Union
from pydantic import BaseModel
from datetime import datetime


class MetricsOut(BaseModel):
    files_processed: int
    min_time_processed: float
    avg_time_processed: float
    max_time_processed: float
    latest_file_processed_timestamp: datetime


class OutputResults(BaseModel):
    results: list[dict[str, Union[str, list[str]]]]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                        'results': [
                            {
                                'name': 'word1',
                                'tf': [
                                    '0.33333 для файла Test1.txt'
                                ],
                                'idf': '0.47712'
                            },
                            {
                                'name': 'word2',
                                'tf': [
                                    '0.33333 для файла Test1.txt',
                                    '0.5 для файла Test2.txt'
                                ],
                                'idf': '0.17609'
                            },
                            {
                                'name': 'word3',
                                'tf': [
                                    '0.33333 для файла Test1.txt',
                                    '1.0 для файла Test3.txt',
                                    '0.5 для файла Test2.txt'
                                ],
                                'idf': '0.0'
                            }
                        ]
                }
            ]
        }
    }

