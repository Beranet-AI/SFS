# Incident Response Guide

This document defines how operational incidents are handled.

---

## Incident Categories

### 1. Data Ingestion Failure
Symptoms:
- No new telemetry
- Edge nodes reporting errors

Actions:
1. Check data_ingestion logs
2. Verify edge connectivity
3. Restart ingestion service if needed

---

### 2. Management Service Failure
Symptoms:
- API errors
- Incidents not created

Actions:
1. Check database connectivity
2. Inspect migration status
3. Restart management container

---

### 3. Monitoring Failure
Symptoms:
- Dashboard not updating
- LiveStatus unavailable

Actions:
1. Check monitoring service
2. Verify cache state
3. Restart monitoring service

---

### 4. AI Decision Failure
Symptoms:
- Health predictions unavailable

Actions:
1. Disable AI service
2. Fall back to rule-based evaluation
3. Log incident for later analysis

---

## Post-Incident Actions

- Create incident report
- Review audit logs
- Add preventive measures if needed
