# src/utils/langchain_imports.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Export them as part of the module's namespace
__all__ = [
    "ChatOpenAI",
    "ChatPromptTemplate"
    
    ]