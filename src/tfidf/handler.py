import re
from datetime import datetime, UTC
from pathlib import Path

import aiofiles
from pymorphy3 import MorphAnalyzer
from math import log10
from collections import deque
from nltk.corpus import stopwords

from definitions import ROOT
from tfidf.schemas import DocumentInDb

analyzer = MorphAnalyzer()
STOPWORDS = set(stopwords.words('russian'))


class Word:
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number
        self.tf: float|None = None
        self.idf: float|None = None


def clean_string(string: str) -> str:
    string = re.sub(r'[^\w\s-]', '', string)
    string = string.lower()
    return string


async def merge_files(collection_in: list[DocumentInDb]) -> str:
    date = datetime.now(UTC).strftime('%Y-%m-%d_%H:%M:%S')
    Path(f'{ROOT}/src/files/tmp/{date}').mkdir(parents=True, exist_ok=True)
    path = f'{ROOT}/src/files/tmp/{date}/tmp.txt'

    async with aiofiles.open(path, 'w') as tmp_file:
        for document in collection_in:
            async with aiofiles.open(document.path, 'r') as file:
                async for line in file:
                    await tmp_file.write(line)

    return path


def compute_tf_in_file(words: list[Word]):
    number_of_all_words = len(words)
    for word in words:
        tf = round(word.number/number_of_all_words, 5)
        word.tf = tf


async def analyze_document(file_in: DocumentInDb):
    all_words: dict[str, int] = {}
    async with aiofiles.open(file_in.path, 'r') as file:
        async for line in file:
            line = clean_string(line)
            words = line.split()
            for word in words:
                normal_word = analyzer.parse(word)[0].normal_form
                if normal_word in STOPWORDS:
                    continue
                if normal_word in all_words:
                    all_words[normal_word] += 1
                else:
                    all_words[normal_word] = 1
    result = [Word(name=name, number=number) for name, number in all_words.items()]
    compute_tf_in_file(result)
    return result


async def analyze_collection(
        collection_in: list[DocumentInDb],
        merged_tf: bool = False,
        collection_id: int|None = None
) -> list[dict[int, list[Word]]]:
    collection: deque[list[Word]] = deque()
    number_of_word_in_collection: dict[str,int] = {}
    documents: dict[int, list[Word]] = {}

    if not merged_tf:
        for file in collection_in:
            tf_statistics = await analyze_document(file)
            documents[file.id] = tf_statistics
            collection.append(tf_statistics)
    else:
        tmp_file_path = await merge_files(collection_in)
        file = DocumentInDb(id=0, title='', path=tmp_file_path)
        tf_statistics = await analyze_document(file)
        documents[collection_id] = tf_statistics
        collection.append(tf_statistics)

    for document in collection:
        for word in document:
            if word.name in number_of_word_in_collection:
                number_of_word_in_collection[word.name] += 1
            else:
                number_of_word_in_collection[word.name] = 1

    results: list[dict[int, list[Word]]] = []

    for document_id, words in documents.items():
        sorted_words = sorted(words, key=lambda item: item.tf)[:50]
        for word in sorted_words:
            idf = round(log10(len(collection_in) / number_of_word_in_collection[word.name]), 5)
            word.idf = idf

        results.append({document_id: sorted_words})

    return results
