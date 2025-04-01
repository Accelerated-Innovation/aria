# loaders/base_loader.py
from abc import ABC, abstractmethod
from src.utils.langchain_imports import LangchainDocument

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> list[LangchainDocument]:
        pass
