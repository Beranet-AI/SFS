# Sequence: Telemetry Ingestion

## Purpose
Describe how raw telemetry moves from physical devices into
the core system and becomes usable for evaluation.

---

## Trigger
A device produces a telemetry measurement.

---

## Participants
- Device
- Edge Node
- Edge Controller (FastAPI)
- Data Ingestion (FastAPI)
- Management (Telemetry Context)
- Monitoring (LiveStatus)

---

## Main Flow

1. Device emits telemetry data
2. Edge Node forwards telemetry to Edge Controller
3. Edge Controller validates and forwards telemetry
4. Data Ingestion receives telemetry
5. Data Ingestion forwards telemetry to Management
6. Management persists telemetry
7. Monitoring updates live snapshot

---

## Side Effects
- Telemetry stored immutably
- LiveStatus updated

---

## Failure Handling
- If Monitoring fails, telemetry ingestion continues
- If rule evaluation fails, telemetry still persists

---

## Mapping
- API: POST /api/v1/telemetry/ingest/
- Services:
  - edge_controller
  - data_ingestion
  - management (telemetry)
- Tests:
  - test_ingest_endpoint.py
  - test_sequence_telemetry_flow.py
