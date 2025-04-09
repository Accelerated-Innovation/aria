from fastapi import FastAPI
from src.api.data_access_api import router as data_access_router

app = FastAPI()
app.include_router(data_access_router)
