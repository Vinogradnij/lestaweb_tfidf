from collections import deque

import aiofiles


async def get_frequency(path: str):
    fq: dict[str, int] = {}
    async with aiofiles.open(path, 'r', encoding='utf-8') as file:
        while chunks := await file.read(1024):
            for chunk in chunks:
                if chunk in fq:
                    fq[chunk] += 1
                else:
                    fq[chunk] = 1
    return fq


async def encode(path: str, encoding: dict[str, str]) -> str:
    text = deque()
    async with aiofiles.open(path, 'r', encoding='utf-8') as file:
        while chunks := await file.read(1024):
            for chunk in chunks:
                text.append(encoding[chunk])
    return ''.join(text)