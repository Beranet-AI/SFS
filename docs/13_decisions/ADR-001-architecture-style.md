# ADR-001: Architecture Style

## Status
Accepted

## Context
SFS requires:
- Strong domain modeling
- Clear ownership of data
- Ability to scale ingestion and monitoring independently
- Long-term maintainability

A traditional monolith would limit scalability,
while a fully distributed event-driven system would introduce unnecessary complexity.

## Decision
Adopt a **modular, service-oriented architecture** with:
- A central Management service (Django) as Source of Truth
- Multiple stateless FastAPI services for orchestration and computation
- Clean Architecture applied per service
- DDD principles applied to domain modeling

## Consequences
Positive:
- Clear responsibility boundaries
- Strong domain integrity
- Independent scaling of services

Negative:
- More initial complexity than a monolith
- Requires discipline to avoid architectural drift
