# ARIA: Accelerated Rewards Intelligent Assistant 🚀  
**An Open Reference Architecture + GenAI Developer Learning Journey**

Welcome to **ARIA**, a modern, microservices-based architecture built for developers and teams creating **GenAI-powered assistants**, **RAG pipelines**, and **real-world LLM apps**.

But ARIA is more than just a repo—it's the foundation for an entire **developer learning path**, built through the partnership of [Marty Bradley](https://www.linkedin.com/in/martybradley), GenAI engineer, educator, and [Accelerated Innovation](https://www.acceleratedinnovation.com).

---

## Learn by Building: A GenAI Developer Journey

Each part of ARIA connects directly to a **hands-on course** in Accelerated Innovation's curriculum. Whether you're upskilling your team or leveling up your own career, you’ll walk away with deployable skills and architecture that scales.

| 📚 Course | 🌐 Key ARIA Component |
|----------|------------------------|
| **1. Building a GenAI Q&A Knowledge Assistant** | `rewards-query-service/`, LangChain RAG |
| **2. Building a Multi-Modal RAG Solution** | `data-ingestion-service/` + `embedding-service/` (text, CSV, JSON, APIs) |
| **3. Evaluating & Debugging RAG Applications** | `observability-service/`, LangSmith, Arize integration |
| **4. Advanced Semantic Search & Vector DBs** | `vector-db-service/` with pgvector, PostgreSQL |
| **5. Secure & Responsible AI for Developers** | `api-gateway/` (JWT Auth), observability & ethical guardrails |
| **6. GenAI Architecture for Developers** | All layers — backend, orchestration, data, frontend |
| **7. Graph DB Best Practices** | Optional integrations (e.g. Neo4j) |
| **8. Advanced RAG Solutions & Methods** | Reranking, multi-vector storage, LangChain CustomRetrievers |
| **9. Leveraging Tools and Agents with MCP & A2A** | `agent-orchestrator-service/` with AutoGen |
| **10. Llama Index for Advanced Search** | Plug-in option: swap LangChain with LlamaIndex |
| **11. Building Cost-Effective GenAI Solutions** | Lightweight services, dockerized deploys, infra guidance |

> 💡 Want live training or team workshops? Check out [acceleratedinnovation.com](https://www.acceleratedinnovation.com) or message me on [LinkedIn](https://www.linkedin.com/in/martybradley).

---

## The ARIA Stack

![image](/docs/images/LLM%20app%20arch.png)

### Frontend
- **Tech:** React + TailwindCSS  
- **Role:** Seamless UX for end users and agents

### Middleware & Gateway
- FastAPI + JWT Auth  
- API gateway for validation, auth, and orchestration

### Core Logic Layer
- `agent-orchestrator-service`: multi-agent workflows (AutoGen)
- `rewards-query-service`: RAG + reranking (LangChain or LlamaIndex)

### Data Layer
- `embedding-service`: SentenceTransformers
- `vector-db-service`: PostgreSQL + pgvector
- `data-ingestion-service`: pipelines from JSON, CSV, APIs

### Observability
- `observability-service`: Arize-powered insights on drift, latency, usage

### Infra
- Docker Compose first, Terraform-ready  
- GitHub Workflows for CI/CD

---

## Try It Yourself

```bash
git clone https://github.com/YOUR-HANDLE/aria
cd aria
# then follow setup instructions in docs/setup-guide.md
```

Includes:
- Dockerized services
- Modular folders
- Prebuilt data ingestion flows
- Embedded documentation

---

## About Accelerated Innovation

We help **developers and enterprise teams master GenAI** through architecture, hands-on projects, and live coaching.

- ✅ Courses from beginner to advanced
- 🧠 Role-based training for devs, data teams, and product leaders
- 🌱 Built on real-world patterns (like ARIA) and production lessons

[Learn more & explore offerings](https://www.acceleratedinnovation.com)

---

## Contribute or Learn More

You can:
- Fork the repo
- Use it as a template for your own AI app
- Join the learning journey
- Reach out to collaborate

Drop a ⭐ if you’re into this work—and let’s build the intelligent future together.

## 📘 Continue Learning

Explore how ARIA connects to hands-on GenAI training with Evergreen AI:

- [🔗 ARIA Learning Journey](docs/learning-journey.md)
- [🔗 Accelerated Course Links](docs/course-links.md)

