# transformers/base_transformer.py
from abc import ABC, abstractmethod
from src.utils.langchain_imports import LangchainDocument

class DocumentTransformer(ABC):
    @abstractmethod
    def transform(self, documents: list[LangchainDocument]) -> list[LangchainDocument]:
        pass
