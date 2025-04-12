# main.py
from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv
from src.api.ingestion_api import router as ingestion_router
from src.services.ingestion_service import IngestionService
from src.loaders.docx_loader import DocxLoader
from src.transformers.text_transformer import RecursiveTextSplitterTransformer

# Configure logging explicitly
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables explicitly
load_dotenv()
logger.info("Environment variables loaded")

# Fetch required environment variables
EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL")
DATA_ACCESS_SERVICE_URL = os.getenv("DATA_ACCESS_SERVICE_URL")

if not EMBEDDING_SERVICE_URL:
    logger.error("EMBEDDING_SERVICE_URL is not set!")
    raise ValueError("EMBEDDING_SERVICE_URL environment variable required.")

if not DATA_ACCESS_SERVICE_URL:
    logger.error("DATA_ACCESS_SERVICE_URL is not set!")
    raise ValueError("DATA_ACCESS_SERVICE_URL environment variable required.")

# Explicitly instantiate ingestion service dependencies
loader = DocxLoader()
transformer = RecursiveTextSplitterTransformer()

# Instantiate ingestion service explicitly
ingestion_service = IngestionService(
    loader=loader,
    transformer=transformer,
    embedding_service_url=EMBEDDING_SERVICE_URL,
    data_access_service_url=DATA_ACCESS_SERVICE_URL
)

# Initialize FastAPI app explicitly
app = FastAPI(
    title="Data Ingestion Service",
    description="Service for ingesting documents and delegating embedding/storage",
    version="0.2.0",
    openapi_tags=[
        {"name": "Ingestion", "description": "Operations for ingesting documents"},
        {"name": "Health", "description": "Health check endpoints"},
    ],
)

# Attach ingestion_service instance to app.state (optional, best-practice)
app.state.ingestion_service = ingestion_service

# Include ingestion router explicitly
app.include_router(ingestion_router)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Data Ingestion Service is running"}

logger.info("Data Ingestion Service startup complete")
