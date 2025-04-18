# src/main.py
from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv
from src.api.embedding_api import router as embedding_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Check required environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")

if not OPENAI_API_KEY:
    logger.warning(
        "OPENAI_API_KEY is not set! Embedding operations will fail.")

logger.info("Using embedding model: %s", OPENAI_EMBEDDING_MODEL)

# FastAPI app initialization
app = FastAPI(
    title="Embedding Service",
    description="Service for generating embeddings from text",
    version="0.2.0",
    openapi_tags=[
        {"name": "Embedding", "description": "Operations for generating embeddings"},
        {"name": "Health", "description": "Health check endpoints"},
    ],
)

# Include embedding router
app.include_router(embedding_router, tags=["Embedding"])


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Embedding Service is running"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "config": {
            "embedding_model": OPENAI_EMBEDDING_MODEL
        }
    }

logger.info("Embedding Service startup complete")
