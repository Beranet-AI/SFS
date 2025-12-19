# Sequence: Live Monitoring

## Purpose
Describe how live monitoring data is served to the dashboard.

---

## Trigger
Operator opens dashboard.

---

## Participants
- WebApp
- Monitoring Service
- LiveStatus Cache

---

## Main Flow

1. WebApp requests live status
2. Monitoring reads snapshot from cache
3. Snapshot is returned to WebApp

---

## Constraints
- No persistent state changes
- No rule evaluation
- No incident creation

---

## Mapping
- API: GET /api/v1/livestatus/
- Service: monitoring
- Tests:
  - test_livestatus_readonly.py
