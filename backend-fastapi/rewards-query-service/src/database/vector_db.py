# src/database/vector_db.py

from src.utils.langchain_imports import PGVector, OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

class VectorDB:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"))
        self.conn_str = os.getenv("DB_CONN_STR")
        self.collection_name = os.getenv("ARIA_EMBEDDINGS")

        self.vector_store = PGVector(
            connection=self.conn_str,
            embeddings=self.embeddings,
            collection_name=self.collection_name,
        )

    def similarity_search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)
    
     def similarity_search_by_vector(self, embedding: list[float], k: int = 5):
        return self.vector_store.similarity_search_by_vector(embedding, k=k)
