# Data Ingestion Service
## Responsibilities: Load, Transform

* Loaders: Loads various file formats (Docx, PDF, etc.).
* Transformers: Splits documents, OCR extraction, data cleaning.
* Database: Stores/retrieves embeddings in PGVector.

## 🎯 **Smoke Test Instructions: Data Ingestion Service**
### ✅ Step 1: Start Dependencies (Infrastructure)
Make sure your PostgreSQL (PGVector) container and embedding-service are running first:

```bash
cd infrastructure
docker-compose up -d --build
```
**Verify:**
- Inside Docker aria_pgvector(`localhost:6024:5432`).
- Embedding Service is running (`localhost:8001`).
- Data Ingestion Service is running (`localhost:8002`).
- Data Access Service is running (`localhost:8004`).
---
### ✅ **2. Verify the FastAPI Swagger UI**

Open in your browser:
```
http://localhost:8002/docs
```

- You must see the FastAPI Swagger documentation UI.
---

### ✅ **3. Execute the Smoke Test**
From Swagger UI, test your `/ingest/docx` POST endpoint with this payload:

```json
{
  "file_path": "test_doc.docx"
}
```
* You can put this test document temporarily at your microservice root (same level as src).

---
### ✅ Step 4: Verify Response
Successful response looks like this:

```json
{
  "status": "success",
  "message": "Document ingested successfully."
}
```
---
### ✅ Step 5: Quick DB Check (Optional but recommended)
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

