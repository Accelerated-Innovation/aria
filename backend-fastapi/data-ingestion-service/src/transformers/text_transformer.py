# transformers/text_transformer.py
import logging
from typing import List, Union
from src.utils.langchain_imports import LangchainDocument, RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class TextTransformer:
    """Base class for text transformers"""
    def transform(self, documents: List[LangchainDocument]) -> List[str]:
        """Transform documents into text chunks"""
        raise NotImplementedError("Subclasses must implement transform method")

class RecursiveTextSplitterTransformer(TextTransformer):
    """Transformer that splits text into chunks using RecursiveCharacterTextSplitter"""
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def transform(self, documents: List[LangchainDocument]) -> List[LangchainDocument]:
        """
        Split documents into smaller chunks using RecursiveCharacterTextSplitter
        
        Args:
            documents: List of LangchainDocument objects
            
        Returns:
            List of LangchainDocument objects representing the chunks
        """
        logger.info("Transforming %d documents with chunk size %d", len(documents), self.chunk_size)
        
        # Extract text from documents if needed
        if not isinstance(documents, list):
            documents = [documents]
            
        # Split documents into chunks
        chunks = []
        for doc in documents:
            doc_chunks = self.text_splitter.split_documents([doc])
            chunks.extend(doc_chunks)
            
        logger.info("Split documents into %d chunks", len(chunks))
        return chunks