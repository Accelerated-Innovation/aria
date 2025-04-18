from fastapi import FastAPI
from src.api.data_access_api import router as data_access_router
import logging
import time
import os
import psycopg
from dotenv import load_dotenv

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

# Get database connection parameters
db_user = os.getenv("POSTGRES_USER", "aria_user")
db_password = os.getenv("POSTGRES_PASSWORD", "aria_password")
db_host = os.getenv("POSTGRES_HOST", "postgres_pgvector")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB", "aria_db")

# Wait for database to be ready
max_retries = 10
retry_interval = 3  # seconds

logger.info(f"Waiting for database connection at {db_host}:{db_port}...")
for attempt in range(max_retries):
    try:
        # Try to connect to the database
        conn = psycopg.connect(
            f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
        )
        conn.close()
        logger.info("Database connection successful")
        break
    except Exception as e:
        logger.warning(f"Database connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
        if attempt < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            logger.error("Max retries reached. Could not connect to database.")
            # Continue anyway, let the application handle it

# FastAPI app initialization
app = FastAPI(
    title="Data Access Service",
    description="Service for accessing vector database",
    version="0.2.0",
    openapi_tags=[
        {"name": "Data Access", "description": "Operations for accessing data"},
        {"name": "Health", "description": "Health check endpoints"},
    ],
)

# Include data access router
app.include_router(data_access_router)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Data Access Service is running"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    # Try to connect to the database
    try:
        conn = psycopg.connect(
            f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
        )
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "config": {
            "db_host": db_host,
            "db_port": db_port,
            "db_name": db_name
        }
    }

logger.info("Data Access Service startup complete")
