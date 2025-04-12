# Rewards Query Service
## Responsibilities: Send requests to the embedding service and query the database for relevant rewards information.

TODO: convert this to an MCP Tool to query the database for relevant rewards information.

## 🚀 **Smoke Test Instructions: Rewards Query Service**

### ✅ **1. Start Dependencies (Infrastructure)**

Ensure your PostgreSQL (PGVector) and other related services are running via Docker Compose:

```bash
cd infrastructure
docker-compose up -d --build
```

**Verify:**
- Inside Docker aria_pgvector(`localhost:6024:5432`).
- Rewards Query Service is running (`localhost:8003`).
- Embedding Service is running (`localhost:8002`).
- Data Access Service is running (`localhost:8004`).
---

### ✅ **2. Verify the FastAPI Swagger UI**

Open in your browser:

```
http://localhost:8003/docs
```

- You must see the FastAPI Swagger documentation UI.

---

### ✅ **3. Execute the Smoke Test**

From Swagger UI, test your `/query_rewards` POST endpoint with this payload:

```json
{
  "query": "Find rewards related to flights and travel.",
  "top_k": 3
}
```

- Click **"Execute"**  in Swagger.

---

### ✅ **4. Verify the Response**

Expect a response formatted similar to:

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

### ✅ **5. Verify Terminal Output (optional but recommended)**

Check your `docker logs rewards-query-service` to verify print statements or logs are appearing clearly:

```
REWARDS QUERY SERVICE STARTING...
INFO: POST /query_rewards
```

---

## 🚩 **Clearly Summarized Workflow:**

| Step                      | Action                                                    | Expectation                  |
|---------------------------|-----------------------------------------------------------|------------------------------|
| Infrastructure            | Start Docker dependencies                                 | Services running             |
| Rewards Query Service     | docker-compose up -d --build                              | Running on port 8003         |
| FastAPI Swagger UI        | Open `localhost:8003/docs`                                | Swagger UI loads             |
| Execute Smoke Test        | Call `/query_rewards` with provided payload               | Returns relevant results     |
| Terminal Check            | Verify service logs                                       | Logs appear clearly          |

---