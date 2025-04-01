# Data Ingestion Service
## Responsibilities: Load, Transform)

```
backend-fastapi/data-ingestion-service/
├── src/
│   ├── loaders/
│   ├── transformers/
│   ├── database/
│   ├── services/
│   └── main.py

```

* Loaders: Loads various file formats (Docx, PDF, etc.).
* Transformers: Splits documents, OCR extraction, data cleaning.
* Database: Stores/retrieves embeddings in PGVector.

## 🎯 How to Smoke Test Your data-ingestion-service:
### ✅ Step 1: Start Dependencies (Infrastructure)
Make sure your PostgreSQL (PGVector) container and embedding-service are running first:

```bash
cd infrastructure
docker-compose up -d postgres_pgvector embedding-service
```
Ensure services are up:
* PGVector: localhost:5432
* Embedding-service: localhost:8001/docs (Swagger API)
---
### ✅ Step 2: Run Your data-ingestion-service
Either manually (via start.sh) or Docker Compose:

**Option A: Local development (manual)**
```bash
cd backend-fastapi/data-ingestion-service/scripts
./start.sh
```

**Option B: Docker Compose**
From infrastructure folder:

```bash
docker-compose up -d data-ingestion-service
```
Your service should now run on:

* localhost:8000/docs (FastAPI interactive docs)
---

### ✅ Step 3: Smoke Test via FastAPI Interactive Docs
1. Open your FastAPI Swagger UI:
http://localhost:8000/docs

2. Execute a basic API call (POST /ingest/docx):

For example, if you have a simple Word document (test_doc.docx) located in your service directory, send a request like:

```json
{
  "file_path": "test_doc.docx"
}
```
* You can put this test document temporarily at your microservice root (same level as src).

3. Verify successful response:

```json
{
  "status": "success",
  "message": "Document ingested successfully."
}
```
### ✅ Step 4: Quick DB Check (Optional but recommended)
Verify embeddings were stored correctly by querying PostgreSQL quickly:

* Connect to your PostgreSQL container:

```bash
docker exec -it aria_pgvector psql -U aria_user -d aria_db
```
* Verify data insertion into your embeddings collection:

```sql
SELECT count(*) FROM langchain_pg_embedding;  -- or your specific table name
```
This simple count query confirms embeddings are stored as expected.
---

### ✅ What you're validating with this Smoke Test:
* Your microservice starts without issues.
* API endpoints function correctly and accept expected parameters.
* Integration with embedding-service and PGVector database works as intended.
* Embeddings are successfully generated, received, and stored.

