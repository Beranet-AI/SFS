# API Overview

The Smart Farm System exposes APIs as **explicit contracts**
between bounded contexts and external consumers.

API principles:
- Resource-oriented endpoints
- Explicit actions for state transitions
- No domain logic in controllers
- DTO-based input/output
- Versioned APIs

All APIs are accessed via HTTPS and are versioned under `/api/v1/`.

Ownership rules:
- Management APIs own write operations
- FastAPI services orchestrate and compute
- Frontend consumes APIs only through published contracts
