# src/embedder/base_embedder.py
from abc import ABC, abstractmethod
from typing import List

class Embedder(ABC):
    @abstractmethod
    def embed(self, documents: List[str]):
        pass
