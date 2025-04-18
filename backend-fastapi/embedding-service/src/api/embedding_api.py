# src/api/embedding_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from src.embedder.openai_embedder import OpenAIEmbedder

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()

class EmbedRequest(BaseModel):
    texts: List[str]

class SingleTextEmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]

class SingleEmbedResponse(BaseModel):
    embedding: List[float]

embedder = OpenAIEmbedder()

@router.post("/embed", response_model=EmbedResponse)
def get_embeddings(request: EmbedRequest):
    """
    Generate embeddings for multiple text strings
    
    Args:
        request: EmbedRequest containing a list of text strings
        
    Returns:
        EmbedResponse with a list of embedding vectors
    """
    try:
        logger.info("Generating embeddings for %d texts", len(request.texts))
        embeddings = embedder.embed(request.texts)
        logger.info("Successfully generated %d embeddings", len(embeddings))
        return {"embeddings": embeddings}
    except Exception as e:
        logger.error("Error generating embeddings: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.post("/embed_query", response_model=SingleEmbedResponse)
def get_query_embedding(request: SingleTextEmbedRequest):
    """
    Generate an embedding for a single query text
    
    Args:
        request: SingleTextEmbedRequest containing a single text string
        
    Returns:
        SingleEmbedResponse with a single embedding vector
    """
    try:
        logger.info("Generating embedding for query: '%s...' (truncated)", request.text[:50])
        embedding = embedder.embed_query(request.text)
        logger.info("Successfully generated embedding of dimension %d", len(embedding))
        return {"embedding": embedding}
    except Exception as e:
        logger.error("Error generating query embedding: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/embed_single", response_model=SingleEmbedResponse)
def get_single_embedding(request: SingleTextEmbedRequest):
    """
    Alternative endpoint to generate an embedding for a single text
    
    Args:
        request: SingleTextEmbedRequest containing a single text string
        
    Returns:
        SingleEmbedResponse with a single embedding vector
    """
    try:
        logger.info("Generating embedding for single text: '%s...' (truncated)", request.text[:50])
        # Use embed_query for single text embedding
        embedding = embedder.embed_query(request.text)
        logger.info("Successfully generated embedding of dimension %d", len(embedding))
        return {"embedding": embedding}
    except Exception as e:
        logger.error("Error generating single text embedding: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
