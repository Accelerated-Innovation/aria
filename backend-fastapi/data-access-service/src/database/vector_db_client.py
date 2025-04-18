from src.utils.langchain_imports import PGVector
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class VectorDBClient:
    def __init__(self):
        # Get database connection parameters from environment variables
        db_user = os.getenv("POSTGRES_USER", "aria_user")
        db_password = os.getenv("POSTGRES_PASSWORD", "aria_password")
        db_host = os.getenv("POSTGRES_HOST", "postgres_pgvector")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "aria_db")
        self.collection_name = os.getenv("ARIA_EMBEDDINGS", "aria_embeddings")
        
        # Construct the connection string explicitly
        connection_string = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        logger.info("Connecting to database at %s:%s/%s", db_host, db_port, db_name)
        
        # Create the PGVector instance with explicit connection string
        try:
            self.vector_store = PGVector(
                connection=connection_string,
                embeddings=None,  # embeddings generated externally via embedding-service
                collection_name=self.collection_name,
                use_jsonb=True
            )
            logger.info("Successfully connected to vector database")
        except Exception as e:
            logger.error("Failed to connect to vector database: %s", str(e))
            # Re-raise the exception with more context
            raise RuntimeError(f"Vector database connection failed: {str(e)}") from e

    def store_embeddings(self, texts: list[str], embeddings: list[list[float]]):
        """
        Store text and embeddings in the vector database
        
        Args:
            texts: List of text strings
            embeddings: List of embedding vectors generated by the embedding-service
            
        Returns:
            Result of the add_embeddings operation
        """
        logger.info("Storing %d texts with embeddings", len(texts))
        return self.vector_store.add_embeddings(texts=texts, embeddings=embeddings)

    def similarity_search_by_vector(self, embedding: list[float], k: int = 5):
        """
        Search for similar embeddings using a raw vector
        
        Args:
            embedding: The query embedding vector generated by the embedding-service
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        logger.info("Performing similarity search with vector of length %d", len(embedding))
        results = self.vector_store.similarity_search_by_vector(embedding, k=k)
        logger.info("Found %d similar documents", len(results))
        return results
