import requests
import logging
import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class RewardsQueryService:
    def __init__(
        self,
        embedding_service_url: str = None,
        data_access_service_url: str = None
    ):
        # Use environment variables with proper container names if URLs not provided
        self.embedding_service_url = embedding_service_url or os.getenv(
            "EMBEDDING_SERVICE_URL"
        )
        self.data_access_service_url = data_access_service_url or os.getenv(
            "DATA_ACCESS_SERVICE_URL"
        )
        
        logger.info("Initialized with embedding service URL: %s", self.embedding_service_url)
        logger.info("Initialized with data access service URL: %s", self.data_access_service_url)

    def get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding vector for a query string using the dedicated query embedding endpoint
        
        Args:
            query: User query string
            
        Returns:
            Embedding vector as a list of floats
        """
        logger.info("Getting embedding for query: '%s'", query)
        
        try:
            # Use the dedicated embed_query endpoint for single text embedding
            logger.info("Sending request to %s/embed_query", self.embedding_service_url)
            response = requests.post(
                f"{self.embedding_service_url}/embed_query", 
                json={"text": query},
                timeout=10
            )
            response.raise_for_status()
            
            # The response format is {"embedding": [...]}
            embedding = response.json()["embedding"]
            logger.info("Successfully retrieved embedding vector of length %d", len(embedding))
            
            # Validate embedding format
            if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
                logger.error("Invalid embedding format: %s", type(embedding))
                logger.error("Embedding sample: %s", str(embedding[:5]) + "..." if embedding else "None")
                raise ValueError("Invalid embedding format received from embedding service")
            
            return embedding
            
        except requests.exceptions.RequestException as e:
            logger.error("Error getting query embedding: %s", str(e))
            if hasattr(e, 'response') and e.response:
                logger.error("Response status: %s", e.response.status_code)
                try:
                    logger.error("Response body: %s", e.response.text)
                except:
                    logger.error("Could not read response body")
            raise

    def query_rewards(self, user_query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query rewards based on user input
        
        Args:
            user_query: User query string
            top_k: Number of results to return
            
        Returns:
            List of reward items matching the query
        """
        logger.info("Processing rewards query: '%s' (top_k=%d)", user_query, top_k)
        
        try:
            # Get embedding for the query
            query_embedding = self.get_query_embedding(user_query)
            
            # Log embedding details for debugging
            logger.info("Embedding dimension: %d", len(query_embedding))
            logger.info("Embedding sample: %s", str(query_embedding[:5]) + "...")
            
            # Prepare request payload
            payload = {
                "embedding": query_embedding,
                "top_k": top_k
            }
            
            # Log request details
            logger.info("Sending similarity search request to: %s/similarity_search_vector", self.data_access_service_url)
            logger.info("Request payload structure: %s", {k: type(v).__name__ for k, v in payload.items()})
            
            # Request similar rewards from data access service
            response = requests.post(
                f"{self.data_access_service_url}/similarity_search_vector",
                json=payload,
                timeout=15
            )
            
            # Check for error response
            if response.status_code != 200:
                logger.error("Data access service returned error status: %d", response.status_code)
                logger.error("Response body: %s", response.text)
                response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            
            # Validate response structure
            if "results" not in response_data:
                logger.error("Invalid response format: 'results' key missing")
                logger.error("Response keys: %s", list(response_data.keys()))
                raise ValueError("Invalid response format from data access service")
            
            results = response_data["results"]
            logger.info("Received %d reward results", len(results))
            
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error("Connection error: %s", str(e))
            # Add more detailed error information for debugging
            if hasattr(e, 'response') and e.response:
                logger.error("Response status: %s", e.response.status_code)
                try:
                    logger.error("Response body: %s", e.response.text)
                    # Try to parse JSON for more details
                    try:
                        error_json = e.response.json()
                        logger.error("Error details: %s", json.dumps(error_json, indent=2))
                    except:
                        pass
                except:
                    logger.error("Could not read response body")
            raise

    def get_reward_details(self, reward_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific reward
        
        Args:
            reward_id: Unique identifier for the reward
            
        Returns:
            Detailed reward information
        """
        logger.info("Fetching details for reward ID: %s", reward_id)
        
        try:
            # Request reward details from data access service
            logger.info("Requesting reward details from %s/get_reward/%s", self.data_access_service_url, reward_id)
            response = requests.get(
                f"{self.data_access_service_url}/get_reward/{reward_id}",
                timeout=10
            )
            
            # Check for error response
            if response.status_code != 200:
                logger.error("Data access service returned error status: %d", response.status_code)
                logger.error("Response body: %s", response.text)
                response.raise_for_status()
                
            reward_details = response.json()
            logger.info("Successfully retrieved details for reward ID: %s", reward_id)
            
            return reward_details
            
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching reward details: %s", str(e))
            if hasattr(e, 'response') and e.response:
                logger.error("Response status: %s", e.response.status_code)
                try:
                    logger.error("Response body: %s", e.response.text)
                except:
                    logger.error("Could not read response body")
            raise

    def get_recommended_rewards(self, user_id: str, count: int = 3) -> List[Dict[str, Any]]:
        """
        Get personalized reward recommendations for a user
        
        Args:
            user_id: Unique identifier for the user
            count: Number of recommendations to return
            
        Returns:
            List of recommended rewards
        """
        logger.info("Generating %d reward recommendations for user: %s", count, user_id)
        
        try:
            # Request recommendations from data access service
            logger.info("Requesting recommendations from %s/recommend_rewards", self.data_access_service_url)
            response = requests.post(
                f"{self.data_access_service_url}/recommend_rewards",
                json={"user_id": user_id, "count": count},
                timeout=15
            )
            
            # Check for error response
            if response.status_code != 200:
                logger.error("Data access service returned error status: %d", response.status_code)
                logger.error("Response body: %s", response.text)
                response.raise_for_status()
                
            response_data = response.json()
            
            # Validate response structure
            if "recommendations" not in response_data:
                logger.error("Invalid response format: 'recommendations' key missing")
                logger.error("Response keys: %s", list(response_data.keys()))
                raise ValueError("Invalid response format from data access service")
                
            recommendations = response_data["recommendations"]
            logger.info("Received %d reward recommendations for user: %s", len(recommendations), user_id)
            
            return recommendations
            
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching reward recommendations: %s", str(e))
            if hasattr(e, 'response') and e.response:
                logger.error("Response status: %s", e.response.status_code)
                try:
                    logger.error("Response body: %s", e.response.text)
                    # Try to parse JSON for more details
                    try:
                        error_json = e.response.json()
                        logger.error("Error details: %s", json.dumps(error_json, indent=2))
                    except:
                        pass
                except:
                    logger.error("Could not read response body")
            raise

