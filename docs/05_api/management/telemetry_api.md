
---

# 🟨 Ingestion APIs (FastAPI)

## `docs/05_api/ingestion/telemetry_api.md`

```md
# Telemetry Ingestion API

Base Path: `/api/v1/telemetry/`

---

## POST /telemetry/ingest/
Ingests telemetry forwarded by edge nodes.

**Request**
```json
{
  "device_id": "dev-9",
  "livestock_id": "cow-42",
  "metric": "temperature",
  "value": 41.2,
  "timestamp": "2025-01-01T09:59:00Z"
}

Behavior

Validates payload
Forwards telemetry to Management
Triggers rule evaluation
Updates live status

Guarantees

Idempotent ingestion (best-effort)
No direct persistence

Mapping

Service: data_ingestion
Sequence: Telemetry Ingestion
Tests: test_ingest_endpoint.py