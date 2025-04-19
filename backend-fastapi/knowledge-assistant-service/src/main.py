from fastapi import FastAPI
import logging
from dotenv import load_dotenv
from src.api.knowledge_api import router as knowledge_router
from src.services.knowledge_service import KnowledgeService

# Load environment explicitly
load_dotenv()

# Setup logging explicitly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app explicitly
app = FastAPI(
    title="Knowledge Assistant Service",
    description="Service for answering questions using embedded knowledge retrieval and LLM generation.",
    version="0.1.0"
)

# Initialize service explicitly and attach it to app state
app.state.knowledge_service = KnowledgeService()

# Include router explicitly
app.include_router(knowledge_router)

@app.get("/")
def root():
    return {"status": "Knowledge Assistant Service is running!"}
