# src/utils/langchain_imports.py

from langchain_core.documents import Document as LangchainDocument
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter 



# Export them as part of the module's namespace
__all__ = [
    "LangchainDocument", 
    "Docx2txtLoader",
    "MarkdownHeaderTextSplitter",
    "RecursiveCharacterTextSplitter",
    ]