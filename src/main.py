from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import db_handler
from tfidf.router import router as api_router
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_handler.dispose()

app_main = FastAPI(
    lifespan=lifespan,
)
app_main.include_router(
    api_router,
    prefix=settings.api.prefix
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app_main',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
