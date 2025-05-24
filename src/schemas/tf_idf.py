from typing import Union

from pydantic import BaseModel


class OutputResults(BaseModel):
    results: list[dict[str, Union[str, list[str]]]]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'results': [
                        {
                            'name': 'предвидеть',
                            'tf': ['0.00585 для файла OneginKTatyane.txt'],
                            'idf': '0.30103'
                         },
                        {
                            'name': 'оскорбить',
                            'tf': ['0.00585 для файла OneginKTatyane.txt'],
                            'idf': '0.30103'
                         },
                    ],
                }
            ]
        }
    }

