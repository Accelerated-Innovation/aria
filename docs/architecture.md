React Frontend
     │
     │ HTTP (JWT)
     ▼
┌──────────────────────────┐
│        API Gateway       │
└────────────┬─────────────┘
             │
             │ HTTP Request (JWT-authenticated)
             ▼
┌───────────────────────────────────┐
│     Knowledge Assistant Service   │
└───────────┬─────────────┬─────────┘
            │             │
            │ HTTP        │ HTTP
            ▼             ▼
 ┌───────────────┐ ┌─────────────────────┐
 │Embedding Svc  │ │Rewards Query Svc    │
 └───────────────┘ └─────────────────────┘
            │              │
            ▼              ▼
    ┌──────────────┐  ┌───────────────────┐
    │Vector DB Svc │  │Vector DB Svc      │
    │(pgVector DB) │  │(pgVector DB)      │
    └──────────────┘  └───────────────────┘


## Multi-Module Architecture
backend-fastapi/
├── api-gateway/
├── rewards-query-service/
├── agent-orchestrator-service/
├── embedding-service/
├── data-ingestion-service/     # ← Expanded Multimodal ingestion capability
│   ├── src/
│   │   ├── loaders/            
│   │   │   ├── text_loader.py
│   │   │   ├── pdf_loader.py          # PDFs (text + images extraction)
│   │   │   ├── ppt_loader.py          # PowerPoint (text, images)
│   │   │   ├── image_loader.py        # Image extraction (OCR-based)
│   │   │   └── video_loader.py        # Video transcript + keyframes
│   │   │
│   │   ├── transformers/
│   │   │   ├── text_transformer.py
│   │   │   ├── image_transformer.py
│   │   │   └── video_transformer.py
│   │   │
│   │   ├── embedder/
│   │   │   ├── text_embedder.py       # SentenceTransformers
│   │   │   ├── image_embedder.py      # CLIP or similar multimodal models
│   │   │   └── multimodal_embedder.py # Combines embeddings if needed
│   │   │
│   │   ├── database/
│   │   │   └── multimodal_vector_db.py  # Store multimodal vectors in pgvector
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── README.md
├── observability-service/
├── knowledge-assistant-service/
└── common/

## Data Access Service
- **Data Access Service**: This service is responsible for managing the data access layer, including database connections and queries. It abstracts the underlying database technology (e.g., PostgreSQL with pgVector) and provides a unified interface for other services to interact with the data.
- **Database**: The data access service uses a PostgreSQL database with pgVector to store and manage multimodal data. The database is designed to support efficient storage and retrieval of multimodal data, including text, images, and videos.
- **Data Models**: The data access service defines data models for the multimodal data, including text, images, and videos. These models are used to represent the data in a structured format that can be easily queried and manipulated.
- **Data Access Layer**: The data access layer provides a set of APIs for other services to interact with the database. This includes APIs for creating, reading, updating, and deleting multimodal data. The data access layer also includes APIs for querying the database using various criteria, such as keywords or tags.
- **Data Ingestion**: The data access service includes functionality for ingesting multimodal data into the database. This includes APIs for uploading text, images, and videos, as well as APIs for processing and embedding the data using machine learning models.
- **Data Retrieval**: The data access service provides APIs for retrieving multimodal data from the database. This includes APIs for searching and filtering data based on various criteria, such as keywords or tags. The data retrieval functionality is designed to be efficient and scalable, allowing for quick access to large volumes of multimodal data.

Frontend
  │
API Gateway (future)
  │
├─ data-ingestion-service ──► embedding-service (generates embeddings)
│          │                            │
│          └───────────► data-access-service (stores embeddings)
│
└─ rewards-query-service ───► embedding-service (generates query embeddings)
           │                            │
           └───────────► data-access-service (retrieves embeddings via similarity search)


