# services/ingestion_service.py
import requests

class IngestionService:
    def __init__(self, loader, transformer, vector_db, embedding_service_url):
        self.loader = loader
        self.transformer = transformer
        self.vector_db = vector_db
        self.embedding_service_url = embedding_service_url

    def ingest(self, file_path: str):
        documents = self.loader.load(file_path)
        chunks = self.transformer.transform(documents)

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self._get_embeddings(texts)
        self.vector_db.store(chunks, embeddings)

    def _get_embeddings(self, texts: list[str]):
        response = requests.post(
            f"{self.embedding_service_url}/embed",
            json={"texts": texts}
        )
        response.raise_for_status()  # robust error handling
        return response.json()["embeddings"]

