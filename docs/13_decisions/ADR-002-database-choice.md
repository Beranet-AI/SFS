# ADR-002: Database Choice

## Status
Accepted

## Context
SFS requires:
- Strong relational integrity
- Mature migration tooling
- Clear ownership of data
- Compatibility with Django ORM

Time-series databases were considered for telemetry,
but operational simplicity and consistency were prioritized.

## Decision
Use **PostgreSQL** as the primary and only persistent data store.

Telemetry is stored relationally with:
- Proper indexing
- Retention policies
- Archival strategies

## Consequences
Positive:
- Single Source of Truth
- Simplified backups and restores
- Strong transactional guarantees

Negative:
- Requires careful indexing for high-volume telemetry
- Future need for optimization or partitioning
