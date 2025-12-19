# Monitoring & Logging

Observability is critical for SFS due to real-time data ingestion.

---

## Logging Strategy

### Application Logs
- Structured logs (JSON)
- Include request id and correlation id
- Include livestock_id when applicable

### Error Logs
- Explicit error codes
- Stack traces in non-production only

---

## Monitoring Metrics

### System Metrics
- CPU, memory, container health

### Application Metrics
- Telemetry ingestion rate
- Incident creation rate
- API response latency

---

## Alerting

- Alerts are operational, not domain concepts
- Alerts notify operators of system health issues

---

## Log Retention

- Local: ephemeral
- Staging/Prod: retention policies apply
