# Aggregate: Incident

## Root Entity
Incident

## Identity
- IncidentId

## Attributes
- livestock_id
- severity
- source (rule, AI, manual)
- status
- timestamps

## Lifecycle States
- Open → Acknowledged → Resolved

## Invariants
- An incident cannot be resolved without being open
- State transitions must be explicit

## Code Mapping
- management/apps/incidents/domain/
