```
User Query 
   │
   │ (1) Send query explicitly to embedding-service to generate query embeddings
   │
Embedding-Service
   │
   └── (returns embedding vector)
   │
Knowledge Assistant Service (receives embedding)
   │
   │ (2) Send embedding explicitly to rewards-query-service to retrieve relevant context
   │
Rewards Query Service (retrieval via RAG)
   │
   └── (returns top-k relevant documents/context)
   │
Knowledge Assistant Service (receives context)
   │
   │ (3) Pass query + retrieved context explicitly to OpenAI LLM (with provided system prompt)
   │
OpenAI LLM
   │
   └── (generates concise answer)
   │
Knowledge Assistant Service (final response)
   │
   └── returns concise answer explicitly to user
```