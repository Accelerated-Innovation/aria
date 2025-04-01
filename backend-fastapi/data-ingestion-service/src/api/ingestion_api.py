from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.ingestion_service import IngestionService
import os
import logging

from dotenv import load_dotenv
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

# Create router with proper tags for Swagger UI organization
router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
    responses={404: {"description": "Not found"}}
)

# Define your API request model
class IngestRequest(BaseModel):
    file_path: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "documents/sample.docx"
            }
        }


# Instantiate your ingestion service here or via dependency injection (recommended for prod)
ingestion_service = IngestionService(
    loader=None,  # initialized in main.py
    transformer=None,  # initialized in main.py
    vector_db=None,  # initialized in main.py
    embedding_service_url=os.getenv("EMBEDDING_SERVICE_URL")
)


@router.post("/docx", summary="Ingest a DOCX document", 
             description="Process and store a DOCX document in the vector database",
             response_description="Confirmation of successful ingestion")
async def ingest_docx(request: IngestRequest):
    """
    Ingest a DOCX document into the system.
    
    - Loads the document from the specified file path
    - Transforms the document into chunks
    - Stores the chunks in the vector database
    
    Returns a success message when completed.
    """
    # Your implementation...
    logger.info("Received ingestion request for file: %s", request.file_path)
    
    # Validate dependencies are properly initialized
    if not ingestion_service.loader or not ingestion_service.transformer or not ingestion_service.vector_db:
        logger.error("Ingestion service dependencies not properly initialized")
        raise HTTPException(
            status_code=500,
            detail="Service not properly initialized. Check server logs."
        )
    
    logger.info(f"Starting ingestion process for: {request.file_path}")
    try:
        ingestion_service.ingest(request.file_path)
        logger.info(f"Successfully ingested document: {request.file_path}")
        return {"status": "success", "message": "Document ingested successfully."}
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error during ingestion: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred during ingestion: {str(e)}")


@router.get("/health")
def health_check():
    print("🚨 IN HEALTH CHECK 🚨", flush=True)
    return {"status": "healthy"}

@router.get("/debug-conn")
def debug_conn():
    return {"conn": os.getenv("DB_CONN_STR")}