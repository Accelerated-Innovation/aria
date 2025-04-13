from src.database.vector_db_client import VectorDBClient

class DataAccessService:
    def __init__(self):
        self.db_client = VectorDBClient()

    def insert_embeddings(self, texts: list[str], embeddings: list[list[float]]):
        return self.db_client.store_embeddings(texts, embeddings)

    def query_by_vector(self, embedding: list[float], top_k: int = 5):
        return self.db_client.similarity_search_by_vector(embedding, k=top_k)
