# Entity Relationship Diagram (Conceptual)

This document describes the conceptual ERD.
Implementation details live in Django models.

---

## Entities

### Farm
- id
- name
- metadata

Relationships:
- Farm 1 → N Barns

---

### Barn
- id
- farm_id

Relationships:
- Barn 1 → N Zones

---

### Zone
- id
- barn_id

---

### Livestock
- id
- farm_id
- location (zone)

Relationships:
- Livestock 1 → N Telemetry
- Livestock 1 → N HealthRecords
- Livestock 1 → N Incidents

---

### Device
- id
- device_type
- livestock_id (optional)

---

### Telemetry
- id
- livestock_id
- device_id
- metric
- value
- timestamp

---

### HealthRecord
- id
- livestock_id
- state
- score
- evaluated_at

---

### Incident
- id
- livestock_id
- severity
- source
- status
- timestamps

---

## Notes

- No foreign keys from FastAPI services
- All relations enforced in Management DB
