# ADR-003: Event vs Request-Based Communication

## Status
Accepted

## Context
SFS involves flows that look event-driven (telemetry, incidents),
but also requires strong consistency and traceability.

Full event sourcing or message brokers introduce operational overhead.

## Decision
Adopt a **request-driven architecture with event-like flows**:
- HTTP-based communication between services
- Explicit orchestration in application services
- No event sourcing or message broker in initial phases

Events are treated as:
- Causal flows
- Not persisted domain events

## Consequences
Positive:
- Simpler debugging and traceability
- Easier onboarding
- Clear API contracts

Negative:
- Less decoupling than async event-driven systems
- Future migration to messaging requires refactoring
