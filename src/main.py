from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import db_handler
from tfidf.router import router as api_router
from users.router import router as users_router
from info.router import router as info_router
from config import settings

origins = [
    'http://0.0.0.0',
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_handler.dispose()

app_main = FastAPI(
    lifespan=lifespan,
    version='1.3.0'
)
app_main.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app_main.include_router(
    api_router,
    prefix=settings.api.prefix
)
app_main.include_router(
    users_router,
)
app_main.include_router(
    info_router,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app_main',
        host=settings.run.host,
        port=settings.run.port,
    )
