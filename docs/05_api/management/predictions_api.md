
---

# 🟥 AI Decision APIs (FastAPI)

## `docs/05_api/ai_decision/predictions_api.md`

```md
# AI Decision API

Base Path: `/api/v1/decision/`

---

## POST /decision/health/
Evaluates livestock health using AI models.

**Request**
```json
{
  "livestock_id": "cow-42"
}

Response
{
  "livestock_id": "cow-42",
  "health_state": "critical",
  "confidence": 0.92,
  "evaluated_at": "2025-01-01T10:01:00Z"
}

Behavior

Fetches telemetry history
Runs prediction model
Persists health evaluation via Management
May create incident if critical

Mapping

Service: ai_decision
Sequence: AI Health Prediction
Tests: test_ai_prediction.py