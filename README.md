# Clinical Intelligence Agent (RAG + Insurance Rules)

An AI-powered clinical insurance assistant that answers user questions using:

Medical guidelines (NICE PDFs)

Insurance coverage rules (Silver / Gold plans)

Retrieval-Augmented Generation (RAG)

Human-in-the-loop (HITL) escalation

Full logging and auditing

The system simulates how a health insurance company could automate first-line clinical coverage inquiries while remaining grounded in official medical guidance.

## What This Project Does

Users can ask natural language questions such as:

“Is insulin covered for type 2 diabetes?”

“What do NICE guidelines say about COPD management?”

### The Agent Logic

Retrieves relevant medical guideline chunks from a vector database (using sentence-transformers/all-MiniLM-L6-v2).

Applies insurance coverage rules based on the user’s plan.

Generates a grounded answer using an LLM (gpt-4o-mini).

Assigns an action: answer, clarify, or escalate to human review.

Logs every interaction for audit and monitoring.

## Key Features

Retrieval-Augmented Generation over NICE medical PDFs.

Insurance coverage rules (plan-based).

Agent decision logic:

    Answer

    Clarify vague questions

    Escalate low-confidence queries (HITL)

PostgreSQL + pgvector vector database.

FastAPI backend & React frontend.

Query logging and audit trail with an admin-only logs interface.

End-to-end working system.

## Architecture

### Offline Ingestion Pipeline:

PDFs → Text Extraction → Chunking → Embeddings → PostgreSQL (pgvector)

### Online Query Pipeline:

User (React UI) → FastAPI /ask endpoint → Agent logic (clarification + RAG + rules) → OpenAI LLM → Answer + logging

## Tech Stack

### Backend:

Python & FastAPI

SQLAlchemy (async)

PostgreSQL + pgvector

OpenAI API (gpt-4o-mini)

SentenceTransformers (all-MiniLM-L6-v2 embeddings)

### Frontend:

React (Vite)

Fetch API

### Infrastructure:

Docker (PostgreSQL)

dotenv for secrets

## Project Structure

clinical-intelligence-agent/
├── app/
│   ├── main.py            # FastAPI app
│   ├── agent.py           # Core agent logic
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── db.py              # Database connection
│
├── ingestion/
│   └── ingest_docs.py     # PDF ingestion pipeline
│
├── scripts/
│   ├── seed_users.py
│   ├── seed_coverage_rules.py
│   └── test_agent.py
│
├── frontend/              # React UI
│
├── data/raw_docs/         # NICE PDFs
└── docker-compose.yml     # Infrastructure setup


## Limitations

This project is a prototype and not a production deployment.

Known limitations include:

Confidence score is model-generated rather than computed from similarity metrics.

Clarification detection relies on an LLM, increasing token usage.

No authentication or authorization (users are mocked).

No caching of embeddings or responses.

Token usage is not monitored or rate-limited.

Logs are stored in the main database instead of a dedicated service.

Frontend UI is minimal.

No cloud deployment (runs locally only).

## Future Improvements (Production-Grade Design) 

If deployed in a real organization, the system would include:

### Backend and Infrastructure

Separate logging and monitoring service (ELK stack, Grafana, Prometheus).

Token usage tracking per user & Rate limiting/API gateway.

Redis caching for embeddings and responses.

Background task queue (Celery, Kafka) & CI/CD pipeline.

### Agent Improvements

Confidence computed from vector similarity scores and rule consistency.

Explicit out-of-scope detection and safer medical response policies.

Multi-turn conversation memory.

### Security and Access

User authentication (JWT) and Role-based access control (RBAC).

Encrypted secrets management.

### Monitoring and Analytics

Dashboards for query volume, escalation rate, and cost per user.

### Deployment

Cloud hosting (AWS, GCP, or Azure) with Kubernetes (K8s).

Managed PostgreSQL service & CDN for frontend.

## How to Run Locally

1. Start database: docker-compose up -d
2. Run backend: uvicorn app.main:app --reload
3. Run frontend: cd frontend && npm run dev
4. Test API: # curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"user_id":1,"question":"Is insulin covered for type 2 diabetes?"}'

## Educational Purpose

This project demonstrates RAG system design, agent reasoning, and human-in-the-loop escalation. It is built for learning and portfolio purposes only and does not provide medical or insurance advice.

## Summary

This project is not just an LLM chatbot. It is a full AI system combining rules, retrieval, logging, escalation, and full-stack services. It mirrors real-world enterprise AI architectures at a prototype scale.

## Documentation

- [Overview](docs/overview.md)
- [User Guide](docs/user-guide.md)
- [System Architecture](docs/system-architecture.md)
- [API Reference](docs/api-reference.md)
- [Limitations & Risks](docs/limitations-and-risks.md)
