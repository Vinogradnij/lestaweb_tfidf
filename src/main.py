from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import db_handler
from tfidf.router import router as api_router
from config import settings

app = FastAPI()
app.include_router(
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_handler.dispose()

    api_router,
    prefix=settings.api.prefix
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
