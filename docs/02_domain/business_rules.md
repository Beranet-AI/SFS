# Business Rules

This document defines high-level business rules independent of implementation.

---

## BR-01 Temperature Threshold
If livestock temperature exceeds configured threshold:
- A rule violation is recorded
- An incident MAY be created

---

## BR-02 Health Degradation
If health score declines across evaluations:
- Health state transitions to at-risk or sick
- Persistent degradation may trigger incident

---

## BR-03 Incident Escalation
High or critical incidents:
- Require acknowledgement
- Cannot be auto-resolved

---

## BR-04 Source Traceability
Every incident must be traceable to:
- A rule evaluation
- Or an AI prediction
- Or a manual operator action

---

## Architectural Note
Rules define **conditions**, not **actions**.
Actions (incidents) are explicit decisions handled by the Incident context.
