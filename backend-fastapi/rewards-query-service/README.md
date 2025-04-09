Structure for the rewards-query-service

```
rewards-query-service/
├── src/
│   ├── api/
│   │   └── rewards_api.py
│   ├── database/
│   │   └── vector_db.py
│   ├── services/
│   │   └── rewards_query_service.py
│   └── main.py
├── tests/
├── Dockerfile
└── README.md
```

Here's your **clearly structured, step-by-step smoke test instructions** for your **Rewards Query Service**:

---

# 🚀 **Smoke Test Instructions: Rewards Query Service**

### ✅ **1. Start Dependencies (Infrastructure)**

Ensure your PostgreSQL (PGVector) and other related services (**embedding-service**, **data-ingestion-service**) are running via Docker Compose:

```bash
cd infrastructure
docker-compose up -d postgres_pgvector embedding-service data-ingestion-service
```

**Verify clearly:**
- PostgreSQL PGVector is running (`localhost:6024`).

---

### ✅ **2. Start Rewards Query Service**

Explicitly start your Rewards Query Service using your `start.sh` script:

```bash
cd backend-fastapi/rewards-query-service/scripts
./start.sh
```

Your service clearly starts at:
```
http://localhost:8003/docs
```

---

### ✅ **3. Verify the FastAPI Swagger UI**

Open clearly in your browser:

```
http://localhost:8003/docs
```

- You must clearly see the FastAPI Swagger documentation UI.

---

### ✅ **4. Execute the Smoke Test**

From Swagger UI, explicitly test your `/query_rewards` POST endpoint with this payload:

```json
{
  "query": "Find rewards related to flights and travel.",
  "top_k": 3
}
```

- Click **"Execute"** clearly in Swagger.

---

### ✅ **5. Verify the Response**

Expect a response explicitly formatted similar to:

```json
{
  "results": [
    {
      "content": "Get 20% off on flights booked through our travel rewards partner.",
      "metadata": {
        "source": "flight_rewards.docx"
      }
    },
    {
      "content": "Earn 10x points on all airline purchases made this month.",
      "metadata": {
        "source": "airline_specials.docx"
      }
    },
    {
      "content": "Redeem your rewards points for international travel.",
      "metadata": {
        "source": "international_rewards.docx"
      }
    }
  ]
}
```

---

### ✅ **6. Verify Terminal Output (optional but recommended)**

Check your terminal window running `rewards-query-service` to explicitly verify print statements or logs are appearing clearly:

```
REWARDS QUERY SERVICE STARTING...
INFO: POST /query_rewards
```

---

### ✅ **7. Quick Database Check (optional but recommended)**

Confirm explicitly embeddings are accessible correctly from PGVector:

```bash
docker exec -it aria_pgvector psql -U aria_user -d aria_db
```

Then quickly query your table to confirm embeddings exist:

```sql
SELECT COUNT(*) FROM langchain_pg_embedding;
```

---

## 🚩 **Clearly Summarized Workflow:**

| Step                      | Action                                                    | Expectation                  |
|---------------------------|-----------------------------------------------------------|------------------------------|
| Infrastructure            | Start Docker dependencies clearly                         | Services running             |
| Rewards Query Service     | Run explicitly `./start.sh`                               | Running on port 8003         |
| FastAPI Swagger UI        | Open `localhost:8003/docs` clearly                        | Swagger UI loads             |
| Execute Smoke Test        | Call `/query_rewards` with provided payload               | Returns relevant results     |
| Terminal Check            | Verify service logs clearly                               | Logs appear clearly          |
| Database Check            | Confirm embeddings present                                | Rows exist in table          |

---

Execute this smoke test clearly and confidently now! Let me know how it goes or if you encounter issues.