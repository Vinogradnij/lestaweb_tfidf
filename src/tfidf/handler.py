import re
import aiofiles
from pymorphy3 import MorphAnalyzer
from math import log10
from collections import deque
from nltk.corpus import stopwords

from tfidf.schemas import DocumentInDb

analyzer = MorphAnalyzer()
STOPWORDS = set(stopwords.words('russian'))


class Word:
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number


def clean_string(string: str) -> str:
    string = re.sub(r'[^\w\s-]', '', string)
    string = string.lower()
    return string


def compute_tf_in_file(words: list[Word]):
    number_of_all_words = len(words)
    for word in words:
        tf = round(word.number/number_of_all_words, 5)
        Word.tf = tf


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


async def analyze_collection(collection_in: list[DocumentInDb]):
