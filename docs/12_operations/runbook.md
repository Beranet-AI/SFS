# Operations Runbook – Smart Farm System (SFS)

This runbook provides step-by-step operational guidance
for running and maintaining SFS in production-like environments.

---

## Service Inventory

Critical services:
- management (Django)
- data_ingestion (FastAPI)

Supporting services:
- monitoring (FastAPI)
- ai_decision (FastAPI)
- edge_controller (FastAPI)
- webapp (Next.js + Nginx)

---

## Daily Checks

- All containers running
- Telemetry ingestion rate non-zero
- No failed health checks
- Incident creation functioning

---

## Startup Procedure

1. Start database
2. Run migrations
3. Start management service
4. Start ingestion and edge services
5. Start monitoring and AI services
6. Start webapp

---

## Shutdown Procedure

1. Stop webapp
2. Stop non-critical FastAPI services
3. Stop ingestion after queue drains
4. Stop management
5. Stop database

---

## Log Locations

- Application logs: container stdout
- Audit logs: management database
- Error logs: container logs

---

## Escalation

If a critical service fails:
- Follow incident_response.md
- Notify system owner
