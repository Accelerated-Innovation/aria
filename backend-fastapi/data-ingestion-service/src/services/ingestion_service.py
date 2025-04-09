# services/ingestion_service.py
import requests
import os
from dotenv import load_dotenv
load_dotenv()

class IngestionService:
    def __init__(self):
        self.embedding_service_url = os.getenv("EMBEDDING_SERVICE_URL")
        self.data_access_service_url = os.getenv("DATA_ACCESS_SERVICE_URL")

    def ingest_document(self, texts: list[str]):
        embeddings_response = requests.post(f"{self.embedding_service_url}/embed", json={"texts": texts})
        embeddings_response.raise_for_status()
        embeddings = embeddings_response.json()["embeddings"]

        store_response = requests.post(
            f"{self.data_access_service_url}/store_embeddings",
            json={"texts": texts, "embeddings": embeddings}
        )
        store_response.raise_for_status()
        return store_response.json()
    
