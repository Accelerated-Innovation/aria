# src/api/embedding_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.embedder.openai_embedder import OpenAIEmbedder
from src.utils.langchain_imports import LangchainDocument

router = APIRouter()

class EmbedRequest(BaseModel):
    texts: list[str]

class EmbedResponse(BaseModel):
    embeddings: list[list[float]]

embedder = OpenAIEmbedder()

@router.post("/embed", response_model=EmbedResponse)
def get_embeddings(request: EmbedRequest):
    try:
        # ✅ Correctly extract page_content
        embeddings = embedder.embed(request.texts)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.get("/health")
def health_check():
    print("🚨 IN HEALTH CHECK 🚨", flush=True)
    return {"status": "healthy"}
