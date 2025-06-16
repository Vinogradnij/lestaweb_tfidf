from typing import Union, Sequence
from pydantic import BaseModel


class DocumentInDb(BaseModel):
    id: int
    title: str
    path: str


class DocumentOut(BaseModel):
    id: int
    title: str


class DocumentOnlyIdOut(BaseModel):
    id: int


class CollectionOnlyIdOut(BaseModel):
    documents: Sequence[DocumentOnlyIdOut]


class CollectionOut(BaseModel):
    id: int
    documents: Sequence[DocumentOut]


class AllCollectionOut(BaseModel):
    collections: Sequence[CollectionOut]


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
