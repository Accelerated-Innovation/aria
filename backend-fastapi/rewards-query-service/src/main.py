# src/main.py

from fastapi import FastAPI
from src.api.rewards_api import router as rewards_router

print("REWARDS QUERY SERVICE STARTING...")

app = FastAPI()
app.include_router(rewards_router)
