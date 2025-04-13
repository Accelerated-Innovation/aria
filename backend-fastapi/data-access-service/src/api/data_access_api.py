from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.data_access_service import DataAccessService

router = APIRouter()
service = DataAccessService()

class StoreEmbeddingsRequest(BaseModel):
    texts: list[str]
    embeddings: list[list[float]]

class VectorQueryRequest(BaseModel):
    embedding: list[float]
    top_k: int = 5

@router.post("/store_embeddings")
def store_embeddings(request: StoreEmbeddingsRequest):
    try:
        result = service.insert_embeddings(request.texts, request.embeddings)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/similarity_search_vector")
def similarity_search_vector(request: VectorQueryRequest):
    try:
        results = service.query_by_vector(request.embedding, request.top_k)
        return {"results": [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
