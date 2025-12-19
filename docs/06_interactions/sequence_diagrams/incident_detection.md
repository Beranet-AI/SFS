# Sequence: Incident Detection

## Purpose
Describe how telemetry violations lead to incident creation.

---

## Trigger
Telemetry violates a configured business rule.

---

## Participants
- Data Ingestion
- Management (Telemetry)
- Management (Rules)
- Management (Incidents)
- Monitoring

---

## Main Flow

1. Telemetry is persisted
2. Rules are evaluated against telemetry
3. A rule violation is detected
4. An incident is created
5. Incident status is set to OPEN
6. Monitoring reflects incident count/state

---

## Side Effects
- Incident record created
- Incident linked to source telemetry

---

## Failure Handling
- Rule evaluation failure does not block telemetry storage
- Incident creation failures are logged and surfaced

---

## Mapping
- API: internal rule evaluation
- Contexts:
  - telemetry
  - rules
  - incidents
- Tests:
  - test_telemetry_to_rule.py
  - test_create_incident.py
