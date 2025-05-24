from fastapi import APIRouter
from .tf_idf import router as tf_idf_router

main_router = APIRouter()

main_router.include_router(tf_idf_router)