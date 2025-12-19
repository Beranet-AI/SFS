# Quality Metrics

Quality in SFS is measured by **risk reduction**, not vanity metrics.

---

## Mandatory Metrics

### 1. Architectural Integrity
- No architecture guard test failures
- No forbidden dependencies

---

### 2. Functional Confidence
- All critical sequences covered
- Incident lifecycle fully tested

---

### 3. Reliability Indicators
- Telemetry ingestion success rate
- Incident creation traceability

---

### 4. Test Health
- Flaky tests = zero tolerance
- Test runtime within acceptable limits

---

## Non-Goals

- 100% code coverage
- Snapshot-heavy UI testing

---

## Acceptance Criteria

A release is acceptable only if:
- All architecture tests pass
- All sequence-based tests pass
- No critical paths lack tests
