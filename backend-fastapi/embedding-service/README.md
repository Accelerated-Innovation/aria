# Embedding Service
## Responsibilities: Generate embeddings

* Embedder: Actual embedding logic with OpenAI (or other models).
* API: FastAPI endpoint to expose embedding generation.

## 🚀 **Smoke Test Instructions: Embedding Service**
### ✅ **1. Start Dependencies (Infrastructure)**

Ensure your PostgreSQL (PGVector) and other related services are running via Docker Compose:

```bash
cd infrastructure
docker-compose up -d --build
```

**Verify:**
- Inside Docker aria_pgvector(`localhost:6024:5432`).
- Embedding Service is running (`localhost:8002`).
---

### ✅ **2. Verify the FastAPI Swagger UI**

Open in your browser:

```
http://localhost:8002/docs
```

- You must see the FastAPI Swagger documentation UI.
---

### ✅ **3. Execute the Smoke Test**

From Swagger UI, test your `/embed` POST endpoint with this payload:

```json
{
  "texts": ["Test embedding", "Another test embedding"]
}

```
Click "Execute".

### ✅ Step 4: Verify Response
Successful response looks like this:

```json
{
  "embeddings": [[0.01, 0.02, ...], [0.03, 0.04, ...]]
}
```
Confirm you receive a list of numeric embedding vectors (arrays).

**What to Check:**
* Status Code: 200 OK
* Embeddings: Array of numeric vectors returned.
* No Errors: Ensure no exceptions or internal errors appear.

### ⚠️ Common Issues & Quick Fixes:
* Service not starting: View Docker logs for the embedding-service.
* OpenAI API Key missing: Verify your .env file has OPENAI_API_KEY.
* Endpoint errors: Check terminal logs for any exceptions or FastAPI errors.

