# main.py
from fastapi import FastAPI
import logging
from src.api.ingestion_api import router as ingestion_router
from src.api.ingestion_api import ingestion_service  # Import the service directly
from dotenv import load_dotenv
from src.loaders.docx_loader import DocxLoader
from src.transformers.text_transformer import RecursiveTextSplitterTransformer
from src.database.vector_db import PGVectorDB
from src.services.ingestion_service import IngestionService
import os

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

# Check if critical environment variables are set
db_conn_str = os.getenv("DB_CONN_STR")
if not db_conn_str:
    logger.warning("DB_CONN_STR environment variable is not set!")

embedding_service_url = os.getenv("EMBEDDING_SERVICE_URL")
if not embedding_service_url:
    logger.warning("EMBEDDING_SERVICE_URL environment variable is not set!")

# Create FastAPI app with custom OpenAPI configuration
app = FastAPI(
    title="Data Ingestion Service",
    description="Service for ingesting documents into the vector database",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Ingestion",
            "description": "Operations for ingesting different document types",
        },
        {
            "name": "Health",
            "description": "Health check endpoints",
        },
    ],
)

# Initialize dependencies
logger.info("Initializing dependencies...")
loader = DocxLoader()
transformer = RecursiveTextSplitterTransformer()
vector_db = PGVectorDB(
    conn_str=db_conn_str,
    collection_name="aria_embeddings"
)

# Properly initialize ingestion_service dependencies
ingestion_service.loader = loader
ingestion_service.transformer = transformer
ingestion_service.vector_db = vector_db
ingestion_service.embedding_service_url = embedding_service_url

# Include router - note that we don't add a prefix here since it's defined in the router
app.include_router(ingestion_router)


@app.get("/", tags=["Health"])
def read_root():
    """
    Root endpoint to check if the service is running.
    """
    return {"message": "Data Ingestion Service is running"}


logger.info("Application startup complete")
