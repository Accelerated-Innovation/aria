# transformers/text_transformer.py
from src.utils.langchain_imports import RecursiveCharacterTextSplitter
from .base_transformer import DocumentTransformer

class RecursiveTextSplitterTransformer(DocumentTransformer):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def transform(self, documents):
        return self.splitter.split_documents(documents)
