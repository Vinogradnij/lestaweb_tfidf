import re
from fastapi import UploadFile
from pymorphy3 import MorphAnalyzer
from math import log10
from collections import deque
from nltk.corpus import stopwords


def compute_tfidf(files: list[UploadFile]) -> list[dict]:
    analyzer = Analyzer(files)
    analyzer.traverse()
    results = sorted(analyzer.compute(), key=lambda x: x['idf'], reverse=True)[:50]
    return results


class Analyzer:
    def __init__(self, files: list[UploadFile]):
        self._files = files
        self._words: dict[str: Word] = {}
        self._analyzer = MorphAnalyzer()
        self._count_all_words_in_file: dict[str: int] = {}
        self._stopwords = set(stopwords.words('russian'))

    def traverse(self):
        for uploaded_file in self._files:
            all_words_in_file = 0
            for line in uploaded_file.file:
                line = line.decode()
                line = self.clean_string(line)
                for word in line.split():
                    normal_word = self._analyzer.parse(word)[0].normal_form
                    if normal_word in self._stopwords:
                        continue
                    if normal_word in self._words:
                        self._words[normal_word].add(uploaded_file.filename)
                    else:
                        self._words[normal_word] = Word(normal_word, uploaded_file.filename)
                    all_words_in_file += 1
            self._count_all_words_in_file[uploaded_file.filename] = all_words_in_file

    def compute(self) -> deque[dict]:
        result = deque()
        for word_name, word_class in self._words.items():
            word_tf_idf = word_class.compute_tf_idf(self._count_all_words_in_file)
            result.append(word_tf_idf)
        return result

    @staticmethod
    def clean_string(string: str) -> str:
        string = re.sub(r'[^\w\s-]', '', string)
        string = string.lower()
        return string


class Word:
    def __init__(self, word: str, filename: str):
        self._word = word
        self._count = 1
        self._count_in_files = {filename: 1}

    def add(self, filename: str):
        self._count += 1
        if filename in self._count_in_files:
            self._count_in_files[filename] += 1
        else:
            self._count_in_files[filename] = 1

    def compute_tf_idf(self, files_with_counter):
        result = {'name': self._word, 'tf': []}
        for filename in self._count_in_files.keys():
            tf = round(self._count_in_files[filename] / files_with_counter[filename], 5)
            result['tf'].append(f'{tf} для файла {filename}')
        idf = round(log10(len(files_with_counter)/len(self._count_in_files)), 5)
        result['idf'] = str(idf)
        return result
