# Functional Requirements

This document defines the functional capabilities of the Smart Farm System (SFS).

---

## FR-01 Livestock Telemetry Ingestion
The system shall ingest telemetry data produced by farm devices and edge nodes.

- Telemetry includes metric, value, timestamp, device identifier, and livestock identifier
- Telemetry ingestion shall support high-frequency updates
- Telemetry shall be accepted via HTTP and edge-forwarded channels

**Mapped to:**
- data_ingestion service
- Telemetry API
- Sequence: Telemetry Ingestion

---

## FR-02 Live Monitoring
The system shall provide near real-time visibility of livestock and device status.

- Live status reflects the most recent telemetry values
- Live monitoring shall not modify persisted business data
- Live monitoring shall be read-only

**Mapped to:**
- monitoring service
- LiveStatus domain
- Dashboard UI

---

## FR-03 Rule-Based Incident Detection
The system shall evaluate telemetry against deterministic business rules.

- Rules may trigger incidents when violated
- Rule evaluation shall be auditable
- Rule configuration shall be centrally managed

**Mapped to:**
- rules app (management)
- incidents app
- Sequence: Telemetry → Incident

---

## FR-04 Incident Lifecycle Management
The system shall manage the full lifecycle of incidents.

Incident states:
- Open
- Acknowledged
- Resolved

Operators shall be able to:
- View incidents
- Acknowledge incidents
- Resolve incidents

**Mapped to:**
- incidents app
- Incidents API
- Frontend incident workflow

---

## FR-05 Health Evaluation
The system shall evaluate livestock health over time.

- Health evaluation may be rule-based or AI-based
- Health evaluations shall be persisted
- Health history shall be queryable

**Mapped to:**
- health app
- ai_decision service

---

## FR-06 AI-Assisted Prediction
The system shall support AI-driven health risk prediction.

- Predictions shall produce a confidence score
- Predictions shall not directly mutate core business data
- Critical predictions may result in incidents

**Mapped to:**
- ai_decision service
- Sequence: AI Health Prediction

---

## FR-07 Edge Discovery & Management
The system shall support discovery and monitoring of edge nodes.

- Edge nodes shall register via heartbeat
- Edge discovery events shall be recorded
- Edge nodes shall forward telemetry securely

**Mapped to:**
- edge_controller service

---

## FR-08 Dashboard Visualization
The system shall provide a web-based dashboard.

- Dashboard shall visualize live status, incidents, and health
- Dashboard shall not bypass backend business logic
- Dashboard shall rely on public APIs only

**Mapped to:**
- frontend/webapp
- API layer
