# src/embedder/openai_embedder.py
from src.utils.langchain_imports import OpenAIEmbeddings
from .base_embedder import Embedder
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

class OpenAIEmbedder(Embedder):
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    def embed(self, documents: List[str]):
        return self.embeddings.embed_documents(documents)  # ✅ Exactly correct
