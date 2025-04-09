# src/api/rewards_api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.rewards_query_service import RewardsQueryService

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    results: list[dict]

rewards_service = RewardsQueryService()

@router.post("/query_rewards", response_model=QueryResponse)
def query_rewards(request: QueryRequest):
    try:
        results = rewards_service.query_rewards(request.query, top_k=request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
