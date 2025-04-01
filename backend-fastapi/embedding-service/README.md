# Embedding Service
## Responsibilities: Generate embeddings

```
aria/backend-fastapi/embedding-service/
├── src/
│   ├── embedder/
│   │   ├── base_embedder.py
│   │   └── openai_embedder.py      # ✅ Embedding logic here
│   ├── api/
│   │   └── embedding_api.py        # ✅ API endpoints for embedding requests
│   ├── services/
│   └── main.py
├── tests/
└── Dockerfile

```

* Embedder: Actual embedding logic with OpenAI (or other models).
* API: FastAPI endpoint to expose embedding generation.

## 🎯 Step-by-Step Smoke Test for embedding-service
### ✅ Step 1: Run your Embedding-Service
* Navigate to your embedding-service directory, and start it up locally:

```bash
cd backend-fastapi/embedding-service/scripts
./start.sh
```

Your embedding service should now be running on:

```bash
http://localhost:8001/docs
```
### ✅ Step 2: Verify the FastAPI Service is Up
Open your browser and go to:

```bash
http://localhost:8001/docs
```
You should clearly see the FastAPI Swagger interface.

### ✅ Step 3: Smoke Test the /embed endpoint
Use the interactive Swagger UI (docs) to call the /embed endpoint directly:
* Expand your /embed POST endpoint.
* Click "Try it out".
* Enter test data clearly, like:

```json
{
  "texts": [
    "This is a smoke test.",
    "Embedding service should embed these texts."
  ]
}
```
Click "Execute".

### ✅ Step 4: Verify Response
Successful response looks clearly like this:

```json
{
  "embeddings": [
    [0.01234, 0.56789, ...],  // Vector embedding for first text
    [0.98765, 0.43210, ...]   // Vector embedding for second text
  ]
}
```
Confirm you receive a list of numeric embedding vectors (arrays).

**What to Check Clearly:**
* Status Code: 200 OK
* Embeddings: Array of numeric vectors returned.
* No Errors: Ensure no exceptions or internal errors appear.

### ⚠️ Common Issues & Quick Fixes:
* Service not starting: Ensure virtual environment is active (source .venv/bin/activate).
* OpenAI API Key missing: Verify your .env file clearly has OPENAI_API_KEY.
* Endpoint errors: Check terminal logs for any exceptions or FastAPI errors.

