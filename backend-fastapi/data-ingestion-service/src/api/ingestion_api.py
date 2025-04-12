# api/ingestion_api.py
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from src.services.ingestion_service import IngestionService
import logging

# Configure logger explicitly
logger = logging.getLogger(__name__)

# Create router with explicit tags for Swagger UI organization
router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
    responses={404: {"description": "Not found"}}
)

# Define your API request model explicitly
class IngestRequest(BaseModel):
    file_path: str

    class Config:
        json_schema_extra = {
            "example": {"file_path": "documents/sample.docx"}
        }


# Explicit dependency injection from FastAPI app state (defined in main.py)
def get_ingestion_service(request: Request) -> IngestionService:
    return request.app.state.ingestion_service


@router.post("/docx", 
             summary="Ingest a DOCX document",
             description="Process and store a DOCX document via external services",
             response_description="Confirmation of successful ingestion")
async def ingest_docx(request_body: IngestRequest, ingestion_service: IngestionService = Depends(get_ingestion_service)):
    logger.info("Received ingestion request for file: %s", request_body.file_path)

    try:
        # Explicitly call ingestion service to handle document ingestion
        result = ingestion_service.ingest_document(request_body.file_path)
        logger.info("Successfully ingested document: %s", request_body.file_path)
        return {"status": "success", "message": "Document ingested successfully.", "details": result}

    except FileNotFoundError as e:
        logger.error("File not found: %s", str(e))
        raise HTTPException(status_code=404, detail=str(e)) from e

    except ValueError as e:
        logger.error("Invalid input: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        logger.exception("Unexpected error during ingestion: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"An error occurred during ingestion: {str(e)}"
        ) from e


@router.get("/health", summary="Health Check")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}
