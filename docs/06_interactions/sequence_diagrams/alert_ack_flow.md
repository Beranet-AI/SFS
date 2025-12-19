# Sequence: Incident Acknowledgement & Resolution

## Purpose
Describe how operators interact with incidents.

---

## Trigger
Operator acknowledges or resolves an incident.

---

## Participants
- WebApp (Frontend)
- Management API
- Management (Incidents)

---

## Main Flow (Acknowledge)

1. Operator views incident list
2. Operator clicks "Acknowledge"
3. WebApp sends POST /incidents/{id}/ack/
4. Incident status transitions to ACKNOWLEDGED
5. Timestamp is recorded

---

## Main Flow (Resolve)

1. Operator clicks "Resolve"
2. WebApp sends POST /incidents/{id}/resolve/
3. Incident status transitions to RESOLVED
4. Resolution timestamp is recorded

---

## Invariants
- Only OPEN incidents can be acknowledged
- Only ACKNOWLEDGED incidents can be resolved

---

## Mapping
- API:
  - POST /api/v1/incidents/{id}/ack/
  - POST /api/v1/incidents/{id}/resolve/
- Tests:
  - test_ack_incident.py
  - test_resolve_incident.py
