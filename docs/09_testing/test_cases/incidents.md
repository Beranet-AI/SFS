# Test Cases – Incidents

---

## TC-INC-01 Create Incident from Rule Violation

**Given**
- Telemetry exceeds threshold

**When**
- Rule evaluation is executed

**Then**
- Incident is created with status OPEN

**Mapped To**
- Sequence: Incident Detection
- Tests:
  - test_telemetry_to_rule.py
  - test_create_incident.py

---

## TC-INC-02 Acknowledge Incident

**Given**
- Incident is OPEN

**When**
- Operator acknowledges incident

**Then**
- Status changes to ACKNOWLEDGED
- Acknowledged timestamp is set

**Mapped To**
- Sequence: Alert Ack Flow
- Tests:
  - test_ack_incident.py

---

## TC-INC-03 Resolve Incident

**Given**
- Incident is ACKNOWLEDGED

**When**
- Operator resolves incident

**Then**
- Status changes to RESOLVED
- Resolution timestamp is set

**Mapped To**
- Tests:
  - test_resolve_incident.py

---

## TC-INC-04 Invalid State Transition

**Given**
- Incident is OPEN

**When**
- Resolve is called directly

**Then**
- Operation is rejected

**Mapped To**
- Domain invariant tests
