import aiofiles


async def get_frequency(path):
    fq: dict[str, int] = {}
    async with aiofiles.open(path, 'r', encoding='utf-8') as file:
        while chunks := await file.read(1024):
            for chunk in chunks:
                if chunk in fq:
                    fq[chunk] += 1
                else:
                    fq[chunk] = 1
    return fq
