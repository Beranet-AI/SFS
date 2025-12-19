# Docker & Containerization

Docker is the primary packaging mechanism for SFS services.

---

## Design Principles

- One service per container
- Stateless services whenever possible
- Explicit dependency declaration

---

## Images

- management: Python + Django
- data_ingestion: Python + FastAPI
- monitoring: Python + FastAPI
- ai_decision: Python + FastAPI
- edge_controller: Python + FastAPI
- webapp: Node.js build + Nginx runtime

---

## Docker Compose Responsibilities

- Network creation
- Service discovery
- Volume management
- Local orchestration

---

## Build Rules

- Multi-stage builds for frontend
- Minimal base images
- No build-time secrets

---

## Runtime Rules

- Containers must be restartable
- No local state inside containers
- Health checks required for critical services
