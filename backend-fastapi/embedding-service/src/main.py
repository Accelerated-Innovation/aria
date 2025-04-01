# src/main.py
from fastapi import FastAPI
from src.api.embedding_api import router as embedding_router

app = FastAPI()

app.include_router(embedding_router)
