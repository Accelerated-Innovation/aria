# src/main.py

from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv
from src.api.rewards_api import router as rewards_router
from src.services.rewards_query_service import RewardsQueryService

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

# Check required environment variables explicitly
EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL")
DATA_ACCESS_SERVICE_URL = os.getenv("DATA_ACCESS_SERVICE_URL")

if not EMBEDDING_SERVICE_URL:
    logger.error("EMBEDDING_SERVICE_URL is not set!")
    raise ValueError("EMBEDDING_SERVICE_URL environment variable required.")

if not DATA_ACCESS_SERVICE_URL:
    logger.error("DATA_ACCESS_SERVICE_URL is not set!")
    raise ValueError("DATA_ACCESS_SERVICE_URL environment variable required.")

logger.info("REWARDS QUERY SERVICE STARTING...")

# FastAPI app initialization
app = FastAPI(
    title="Rewards Query Service",
    description="Service for querying rewards data and recommendations",
    version="0.2.0",
    openapi_tags=[
        {"name": "Rewards", "description": "Operations for querying rewards data"},
        {"name": "Health", "description": "Health check endpoints"},
    ],
)

# Initialize dependencies
logger.info("Initializing dependencies...")

# Create the rewards query service instance and store in app state
rewards_service = RewardsQueryService(
    embedding_service_url=EMBEDDING_SERVICE_URL,
    data_access_service_url=DATA_ACCESS_SERVICE_URL
)

# Store the service in app state for dependency injection
app.state.rewards_service = rewards_service

# Include rewards router
app.include_router(rewards_router)
logger.info("Rewards router included")


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Rewards Query Service is running"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "config": {
            "embedding_service_url": EMBEDDING_SERVICE_URL,
            "data_access_service_url": DATA_ACCESS_SERVICE_URL
        }
    }


@app.get("/health/check-connections", tags=["Health"])
async def check_connections():
    """Check connections to dependent services"""
    results = {}

    # Check embedding service
    try:
        import requests
        response = requests.get(f"{EMBEDDING_SERVICE_URL}/health", timeout=5)
        results["embedding_service"] = {
            "status": "up" if response.status_code == 200 else "error",
            "details": response.json() if response.status_code == 200 else str(response.status_code)
        }
    except Exception as e:
        results["embedding_service"] = {
            "status": "down",
            "details": str(e)
        }

    # Check data access service
    try:
        response = requests.get(f"{DATA_ACCESS_SERVICE_URL}/health", timeout=5)
        results["data_access_service"] = {
            "status": "up" if response.status_code == 200 else "error",
            "details": response.json() if response.status_code == 200 else str(response.status_code)
        }
    except Exception as e:
        results["data_access_service"] = {
            "status": "down",
            "details": str(e)
        }

    return {
        "status": "healthy" if all(r["status"] == "up" for r in results.values()) else "unhealthy",
        "services": results,
        "environment": {
            "EMBEDDING_SERVICE_URL": EMBEDDING_SERVICE_URL,
            "DATA_ACCESS_SERVICE_URL": DATA_ACCESS_SERVICE_URL
        }
    }

logger.info("Rewards Query Service startup complete")
