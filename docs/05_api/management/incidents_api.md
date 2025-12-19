
---

## `docs/05_api/management/incidents_api.md`

```md
# Incidents API

Base Path: `/api/v1/incidents/`

---

## GET /incidents/
Returns incidents with optional filters.

Query Params:
- livestock_id
- status
- severity

---

## POST /incidents/{id}/ack/
Acknowledges an incident.

---

## POST /incidents/{id}/resolve/
Resolves an incident.

---

## Response (Incident DTO)
```json
{
  "id": "inc-77",
  "livestock_id": "cow-42",
  "severity": "high",
  "status": "open",
  "source": "rule",
  "created_at": "2025-01-01T10:00:00Z",
  "acknowledged_at": null,
  "resolved_at": null
}

Mapping

Aggregate: Incident
DTO: incident.dto
Sequence: Telemetry → Incident
Tests: test_incident_api.py