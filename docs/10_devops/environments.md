# Environments

SFS supports multiple environments with **identical topology**
and environment-specific configuration.

---

## Environment Types

### Local
- Purpose: Development and testing
- Orchestration: Docker Compose
- Persistence: Local volumes
- Logging: Console

### Staging (Planned)
- Purpose: Integration testing
- Orchestration: Docker Compose / Kubernetes
- Persistence: Managed DB
- Logging: Centralized

### Production (Planned)
- Purpose: Live operations
- Orchestration: Kubernetes
- Persistence: Managed PostgreSQL
- Logging: Centralized + retention policies

---

## Configuration Principles

- No hardcoded configuration
- All environment-specific values via env variables
- `.env.example` documents required configuration

---

## Secrets Management

- Local: `.env` (gitignored)
- Staging/Prod: Secret manager (future)
