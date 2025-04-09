# Installing PostgreSQL & pgVector

To use `pgvector` with PostgreSQL, follow the instructions at  [pgvector GitHub repository](https://github.com/pgvector/pgvector#installation).

NOTE:  We suggest using the Docker installation method for PostgreSQL and pgVector. This method is easier to manage and ensures that both PostgreSQL and pgVector are running in the same container. You can find the installation instructions for Docker at [Docker documentation](https://docs.docker.com/get-docker/).

1. Run the following command to start the container PostgreSQL image from Docker Hub:

```bash
docker compose up -d 
```

2. Use this Docker command to connect to the PostgreSQL database:
```bash
docker exec -it aria_pgvector psql -U aria_user -d aria_db
```

## ✅ Summarized Commands (Clearly Restated Again):
Task	Command
Enter Docker PostgreSQL Container	docker exec -it aria_pgvector psql -U aria_user -d aria_db
List all tables	\dt
Check installed extensions	\dx
Describe specific table	\d aria_embeddings
Exit	\q

