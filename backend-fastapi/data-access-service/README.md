# 🚀 **Smoke Test Instructions: Data Access Service**

Follow these steps to quickly verify the basic functionality of your Data Access Service.

---

## ✅ **1. Start Dependencies (Infrastructure)**

First, ensure your PostgreSQL PGVector database is running:

```bash
cd infrastructure
docker compose up -d 
```

Verify PostgreSQL PGVector is running at:
```
localhost:6024
```

---

## ✅ **2. Start Data Access Service**

From the `data-access-service` directory, start the service:

```bash
cd backend-fastapi/data-access-service/scripts
./start.sh
```

The service should now run at:
```
http://localhost:8004/docs
```

---

## ✅ **3. Verify the FastAPI Swagger UI**

Open your browser and navigate to:
```
http://localhost:8004/docs
```

You should see the interactive Swagger documentation UI.

---

## ✅ **4. Execute the Smoke Test**

### 🔹 **4.1 Test `/store_embeddings` endpoint**

Use the Swagger UI to make a request to the endpoint:
```
POST /store_embeddings
```

#### **Payload example:**

```json
{
  "texts": ["Test embedding storage.", "Second test embedding."],
  "embeddings": [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6]
  ]
}
```

You should receive a success response:

```json
{
  "status": "success",
  "result": [ /* IDs of stored embeddings or similar */ ]
}
```

---

### 🔹 **4.2 Test `/similarity_search_vector` endpoint**

Use the Swagger UI to make a request to the endpoint:
```
POST /similarity_search_vector
```

#### **Payload example:**

```json
{
  "embedding": [0.1, 0.2, 0.3],
  "top_k": 2
}
```

You should see a response containing relevant documents based on similarity search:

```json
{
  "results": [
    {
      "content": "Test embedding storage.",
      "metadata": {}
    },
    {
      "content": "Second test embedding.",
      "metadata": {}
    }
  ]
}
```

---

## ✅ **5. Verify Terminal Logs (recommended)**

Check your terminal running `data-access-service` to verify logs appear correctly:

```
INFO: POST /store_embeddings
INFO: POST /similarity_search_vector
```

---

## ✅ **6. Quick Database Verification (optional but recommended)**

Ensure embeddings were stored correctly by directly querying PGVector:

```bash
docker exec -it aria_pgvector psql -U aria_user -d aria_db
```

Run this command in the PostgreSQL CLI to count embeddings stored:

```sql
SELECT COUNT(*) FROM langchain_pg_embedding;
```

You should see the total number of embeddings reflected.

---

## 🚩 **Quick Reference**

| Step                      | Action                                   | Expectation                        |
|---------------------------|------------------------------------------|------------------------------------|
| Infrastructure            | `docker-compose up -d `                  | PostgreSQL PGVector running        |
| Start Data Access Service | `./start.sh`                             | Service running on port `8004`     |
| FastAPI UI                | `localhost:8004/docs`                    | Swagger UI visible                 |
| Store Embeddings          | POST `/store_embeddings`                 | Success response                   |
| Similarity Search         | POST `/similarity_search_vector`         | Relevant search results            |
| Verify Logs               | View terminal logs                       | Logs clearly displayed             |

---

Execute these smoke test steps now, and you'll quickly confirm your Data Access Service is functioning as expected.


## Rebuild your Docker image after changes:
```bash
docker stop data-access-service
docker rm data-access-service
docker build -t data-access-service:latest .
```

Then run it again with the following command:
```bash
docker run -d -p 8004:8000 --name data-access-service data-access-service:latest
```

View the logs with:
```bash
docker logs -f data-access-service
```
