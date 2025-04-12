# services/ingestion_service.py
import requests
from typing import List

class IngestionService:
    def __init__(
        self,
        loader,
        transformer,
        embedding_service_url: str,
        data_access_service_url: str
    ):
        self.loader = loader
        self.transformer = transformer
        self.embedding_service_url = embedding_service_url
        self.data_access_service_url = data_access_service_url

    def ingest_document(self, file_path: str):
        # Load and transform document explicitly
        document = self.loader.load(file_path)
        texts = self.transformer.transform(document)

        # Explicitly request embeddings from embedding service
        embeddings_response = requests.post(
            f"{self.embedding_service_url}/embed",
            json={"texts": texts},
            timeout=15
        )
        embeddings_response.raise_for_status()
        embeddings = embeddings_response.json()["embeddings"]

        # Explicitly store embeddings via data access service
        store_response = requests.post(
            f"{self.data_access_service_url}/store_embeddings",
            json={"texts": texts, "embeddings": embeddings},
            timeout=15
        )
        store_response.raise_for_status()
        return store_response.json()
