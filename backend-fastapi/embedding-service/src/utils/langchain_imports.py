# src/utils/langchain_imports.py

from langchain_openai import OpenAIEmbeddings

# Export them as part of the module's namespace
__all__ = [
    "OpenAIEmbeddings"
    ]