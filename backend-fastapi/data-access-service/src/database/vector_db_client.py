from src.utils.langchain_imports import PGVector
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDBClient:
    def __init__(self):
        self.conn_str = os.getenv("DB_CONN_STR")
        self.collection_name = os.getenv("ARIA_EMBEDDINGS")
        
        self.vector_store = PGVector(
            connection=self.conn_str,
            embeddings=None,  # embeddints generated externally
            collection_name=self.collection_name,
        )

    def store_embeddings(self, texts: list[str]):
        return self.vector_store.add_texts(texts)
    
    # IMPORTANT: vector_story doesn't explicity embed text internally--this logic
    #            exists in the embedding service.

    def similarity_search_by_vector(self, embedding: list[float], k: int = 5):
        return self.vector_store.similarity_search_by_vector(embedding, k=k)
