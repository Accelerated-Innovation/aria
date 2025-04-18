# src/api/rewards_api.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from src.services.rewards_query_service import RewardsQueryService

# Configure logger
logger = logging.getLogger(__name__)

# Create router with proper tags for Swagger UI organization
router = APIRouter(
    prefix="/rewards",
    tags=["Rewards"],
    responses={404: {"description": "Not found"}}
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "travel discounts in Europe",
                "top_k": 5
            }
        }

class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]

class RecommendationRequest(BaseModel):
    user_id: str
    count: int = 3
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "count": 3
            }
        }

# Dependency to get the rewards service instance
def get_rewards_service():
    """Dependency to get the rewards service instance."""
    return RewardsQueryService()

@router.post("/query", response_model=QueryResponse)
async def query_rewards(request: QueryRequest, rewards_service=Depends(get_rewards_service)):
    """Query rewards based on user input"""
    try:
        logger.info("Received rewards query: '%s' (top_k=%d)", request.query, request.top_k)
        results = rewards_service.query_rewards(request.query, request.top_k)
        logger.info("Returning %d rewards query results", len(results))
        return {"results": results}
    except Exception as e:
        logger.error("Error processing rewards query: %s", str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred during rewards query: {str(e)}") from e

@router.get("/detail/{reward_id}")
async def get_reward_detail(reward_id: str, rewards_service=Depends(get_rewards_service)):
    """Get detailed information about a specific reward"""
    try:
        logger.info("Received request for reward detail: %s", reward_id)
        reward_details = rewards_service.get_reward_details(reward_id)
        logger.info("Successfully retrieved details for reward: %s", reward_id)
        return reward_details
    except Exception as e:
        logger.error("Error retrieving reward details: %s", str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred retrieving reward details: {str(e)}") from e

@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest, rewards_service=Depends(get_rewards_service)):
    """Get personalized reward recommendations for a user"""
    try:
        logger.info(f"Received recommendation request for user: {request.user_id} (count={request.count})")
        recommendations = rewards_service.get_recommended_rewards(request.user_id, request.count)
        logger.info(f"Returning {len(recommendations)} reward recommendations for user: {request.user_id}")
        return {"recommendations": recommendations}
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred generating recommendations: {str(e)}")
