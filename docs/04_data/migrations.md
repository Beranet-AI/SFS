# Database Migrations

Migrations are owned exclusively by the Management service.

---

## Principles

- Migrations reflect domain evolution, not implementation shortcuts
- Each bounded context manages its own migration files
- Breaking migrations require explicit ADR

---

## Structure


Examples:
- livestock/migrations/
- telemetry/migrations/
- incidents/migrations/

---

## Rules

- No migrations in FastAPI services
- No shared database access
- Migration history is part of audit trail

---

## Deployment

- Migrations run before application startup
- Migration failures block deployment
