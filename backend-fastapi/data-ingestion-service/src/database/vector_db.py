# database/vector_db.py
from src.utils.langchain_imports import PGVector
from .base_vector_db import VectorDB

class PGVectorDB(VectorDB):
    def __init__(self, conn_str, collection_name):
        self.conn_str = conn_str
        self.collection_name = collection_name

    def store(self, documents, embeddings):
        vectorstore = PGVector(
            connection=self.conn_str,
            embeddings=None, # Already embedded
            collection_name=self.collection_name
        )
        vectorstore.add_embeddings(texts=[doc.page_content for doc in documents], embeddings=embeddings)
