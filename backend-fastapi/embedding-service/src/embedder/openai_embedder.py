# src/embedder/openai_embedder.py
from src.utils.langchain_imports import OpenAIEmbeddings
from .base_embedder import Embedder
from typing import List
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIEmbedder(Embedder):
    def __init__(self):
        model_name = os.getenv("OPENAI_EMBEDDING_MODEL",
                               "text-embedding-ada-002")
        logger.info("Initializing OpenAIEmbedder with model: %s", model_name)
        self.embeddings = OpenAIEmbeddings(model=model_name)

    def embed(self, documents: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents

        Args:
            documents: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        logger.info("Embedding %d documents", len(documents))
        try:
            result = self.embeddings.embed_documents(documents)
            logger.info("Successfully embedded %d documents", len(documents))
            return result
        except Exception as e:
            logger.error("Error embedding documents: %s", str(e))
            raise

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query text

        Args:
            text: Single text string to embed

        Returns:
            Single embedding vector
        """
        logger.info(f"Embedding single query text: '{text[:50]}...' (truncated)" if len(
            text) > 50 else f"Embedding single query text: '{text}'")
        try:
            result = self.embeddings.embed_query(text)
            logger.info(
                "Successfully embedded query with vector of dimension %d", len(result))
            return result
        except Exception as e:
            logger.error("Error embedding query: %s", str(e))
            raise
