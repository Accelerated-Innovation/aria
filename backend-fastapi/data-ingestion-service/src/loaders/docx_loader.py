# loaders/docx_loader.py
import os
import logging
from src.utils.langchain_imports import Docx2txtLoader
from .base_loader import DocumentLoader

# Configure logger
logger = logging.getLogger(__name__)


class DocxLoader(DocumentLoader):
    def load(self, file_path: str):
        logger.info("Attempting to load document from path: %s", file_path)
        
        # Check if the path is absolute
        if not os.path.isabs(file_path):
            # If it's a relative path, make it absolute from the project root
            base_dir = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))
            absolute_path = os.path.join(base_dir, file_path)
            logger.info("Converting relative path to absolute: %s", absolute_path)
        else:
            absolute_path = file_path
            
        # Verify the file exists
        if not os.path.exists(absolute_path):
            logger.error("File not found: %s", absolute_path)
            raise FileNotFoundError(
                f"The file {file_path} does not exist. Please check the path and try again.")
        
        # Log file details
        file_size = os.path.getsize(absolute_path) / 1024  # KB
        logger.info("Loading document: %s (Size: %.2f KB)", absolute_path, file_size)
        
        try:
            loader = Docx2txtLoader(absolute_path)
            documents = loader.load()
            logger.info("Successfully loaded document with %d sections", len(documents))
            return documents
        except Exception as e:
            logger.exception("Error loading document: %s", str(e))
            raise ValueError(f"Failed to load document: {str(e)}") from e
