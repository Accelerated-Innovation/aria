# services/ingestion_service.py
import requests
import logging
import os
from typing import List, Union
from src.utils.langchain_imports import LangchainDocument

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(
        self,
        loader,
        transformer,
        embedding_service_url: str = None,
        data_access_service_url: str = None
    ):
        self.loader = loader
        self.transformer = transformer
        
        # Use environment variables with proper container names if URLs not provided
        self.embedding_service_url = embedding_service_url or os.getenv(
            "EMBEDDING_SERVICE_URL", "http://embedding-service:8000"
        )
        self.data_access_service_url = data_access_service_url or os.getenv(
            "DATA_ACCESS_SERVICE_URL", "http://data-access-service:8000"
        )
        
        logger.info("Initialized with embedding service URL: %s", self.embedding_service_url)
        logger.info("Initialized with data access service URL: %s", self.data_access_service_url)

    def ingest_document(self, file_path: str):
        """
        Process a document through the ingestion pipeline:
        1. Load the document
        2. Transform it into chunks
        3. Get embeddings for the chunks
        4. Store the chunks and embeddings
        """
        logger.info("Starting ingestion process for %s", file_path)
        
        # Load document
        documents = self.loader.load(file_path)
        logger.info("Loaded %d document sections", len(documents))
        
        # Transform documents into text chunks
        chunks = self.transformer.transform(documents)
        logger.info("Transformed into %d text chunks", len(chunks))
        
        # Extract text content from Document objects or text chunks
        if isinstance(chunks[0], LangchainDocument):
            # If chunks are Document objects, extract their page_content
            texts = [doc.page_content for doc in chunks]
            logger.info("Extracted text content from Document objects")
        else:
            # If chunks are already strings
            texts = chunks
        
        # Request embeddings from embedding service
        logger.info("Requesting embeddings from %s/embed", self.embedding_service_url)
        try:
            embeddings_response = requests.post(
                f"{self.embedding_service_url}/embed",
                json={"texts": texts},
                timeout=15
            )
            embeddings_response.raise_for_status()
            embeddings = embeddings_response.json()["embeddings"]
            logger.info("Received %d embeddings", len(embeddings))
            
            # Store embeddings via data access service
            logger.info("Storing embeddings via %s/store_embeddings", self.data_access_service_url)
            store_response = requests.post(
                f"{self.data_access_service_url}/store_embeddings",
                json={"texts": texts, "embeddings": embeddings},
                timeout=15
            )
            store_response.raise_for_status()
            logger.info("Successfully stored embeddings and text chunks")
            
            return store_response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error("Connection error: %s", str(e))
            # Add more detailed error information for debugging
            if hasattr(e, 'response') and e.response:
                logger.error("Response status: %s", e.response.status_code)
                logger.error("Response body: %s", e.response.text)
            raise