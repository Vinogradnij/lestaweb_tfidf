import re
import aiofiles
from pymorphy3 import MorphAnalyzer
from math import log10
from collections import deque
from nltk.corpus import stopwords

from tfidf.schemas import DocumentInDb

analyzer = MorphAnalyzer()
STOPWORDS = set(stopwords.words('russian'))


def clean_string(string: str) -> str:
    string = re.sub(r'[^\w\s-]', '', string)
    string = string.lower()
    return string


def compute_tf_in_file(words: dict[str, int]) -> dict[str, float]:
    number_of_all_words = len(words)
    all_tf: dict[str, float] = {}

    for word, number_of_word in words.items():
        tf = round(number_of_word/number_of_all_words, 5)
        all_tf[word] = tf

    result = dict(sorted(all_tf.items(), key=lambda statistics: statistics[1])[:50])
    return result



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
    tf_50 = compute_tf_in_file(all_words)
    return tf_50
