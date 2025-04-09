import requests
import os
from dotenv import load_dotenv
load_dotenv()

class RewardsQueryService:
    def __init__(self):
        self.embedding_service_url = os.getenv("EMBEDDING_SERVICE_URL")
        self.data_access_service_url = os.getenv("DATA_ACCESS_SERVICE_URL")

    def get_query_embedding(self, query: str):
        response = requests.post(f"{self.embedding_service_url}/embed", json={"texts": [query]})
        response.raise_for_status()
        return response.json()["embeddings"][0]

    def query_rewards(self, user_query: str, top_k: int = 5):
        query_embedding = self.get_query_embedding(user_query)
        response = requests.post(
            f"{self.data_access_service_url}/similarity_search_vector",
            json={"embedding": query_embedding, "top_k": top_k}
        )
        response.raise_for_status()
        return response.json()["results"]

