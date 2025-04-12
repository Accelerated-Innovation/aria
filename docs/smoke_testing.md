# Smoke Testing
## ✅ Step 1: Clear out the PGVector Database
To reset the database quickly (assuming your PostgreSQL Docker container is named aria_pgvector):

```bash
docker exec -it aria_pgvector psql -U aria_user -d aria_db
```
Run these commands inside the psql shell to drop and recreate the tables:

```sql
-- Drop langchain_pg_embedding table explicitly
DROP TABLE IF EXISTS langchain_pg_embedding CASCADE;

-- (Optional) Recreate the empty table explicitly if required now
CREATE EXTENSION IF NOT EXISTS vector;
```
Confirm it's empty with:

```sql
\dt  -- should show no tables
```
Then exit:

```sql
\q
```

## ✅ [Smoke test the Embedding Service](..\backend-fastapi\embedding-service\README.md)
## ✅ [Smoke test the Data Access Service](..\backend-fastapi\data-access-service\README.md)
## ✅ [Smoke test the Data Ingestion Service](..\backend-fastapi\data-ingestion-service\README.md)
## ✅ [Smoke test the Rewards Query Service](..\backend-fastapi\rewards-query-service\README.md)
