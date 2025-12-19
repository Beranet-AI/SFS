# Test Strategy

SFS testing strategy is **architecture-driven**.
Tests are derived from:
- Bounded contexts
- C4 diagrams
- Sequence diagrams
- Explicit architectural constraints

The goal is not maximum coverage,
but **maximum confidence with minimum fragility**.

---

## Test Levels

### 1. Unit Tests
Purpose:
- Validate domain logic and invariants
- Fast and deterministic

Scope:
- Domain entities
- Value objects
- Pure application services

No:
- Database
- HTTP
- External services

---

### 2. Application / Integration Tests
Purpose:
- Validate use cases across components
- Ensure correct orchestration

Scope:
- Application services
- Multiple apps within Management
- Service-to-service interactions (mocked)

---

### 3. API Tests
Purpose:
- Validate public contracts
- Ensure request/response correctness

Scope:
- Django REST APIs
- FastAPI endpoints

---

### 4. Architecture Guard Tests
Purpose:
- Prevent architectural decay

Scope:
- Dependency direction
- Layer violations
- Forbidden imports

These tests are **merge blockers**.

---

### 5. System / Sequence Tests
Purpose:
- Validate end-to-end flows
- Ensure diagrams reflect reality

Scope:
- Telemetry → Incident
- AI Decision → Incident
- Live Monitoring

---

## Test Ownership

- Domain tests owned by Management
- Orchestration tests owned by FastAPI services
- Contract tests shared across backend and frontend
