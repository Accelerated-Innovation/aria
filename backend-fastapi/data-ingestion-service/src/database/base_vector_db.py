# database/base_vector_db.py
from abc import ABC, abstractmethod

class VectorDB(ABC):
    @abstractmethod
    def store(self, documents, embeddings):
        pass
