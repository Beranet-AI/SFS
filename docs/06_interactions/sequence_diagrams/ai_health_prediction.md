# Sequence: AI Health Prediction

## Purpose
Describe how AI-driven health evaluation is performed.

---

## Trigger
Operator or scheduled job requests health evaluation.

---

## Participants
- WebApp
- AI Decision Service
- Management (Telemetry)
- Management (Health)
- Management (Incidents)

---

## Main Flow

1. WebApp requests health evaluation
2. AI Decision fetches telemetry history
3. AI model evaluates health
4. Health record is created
5. If critical, an incident is created

---

## Side Effects
- Health history updated
- Optional incident creation

---

## Failure Handling
- AI failure does not affect telemetry ingestion
- Health evaluation failure is isolated

---

## Mapping
- API: POST /api/v1/decision/health/
- Service: ai_decision
- Tests:
  - test_ai_prediction_creates_incident.py
