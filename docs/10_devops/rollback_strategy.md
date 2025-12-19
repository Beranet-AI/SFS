# Rollback Strategy

Rollback is a first-class operational concern.

---

## Principles

- Prefer roll-forward fixes
- Rollback must be safe and fast
- Data integrity must never be compromised

---

## Application Rollback

- Re-deploy previous container image
- Stateless services restart safely

---

## Database Rollback

- No automatic rollback of migrations
- Rollback requires:
  - Explicit migration
  - ADR documentation

---

## Failure Scenarios

### AI Decision Failure
- Disable AI service
- System continues with rule-based logic

### Monitoring Failure
- Live dashboard degraded
- Core ingestion unaffected

---

## Verification

After rollback:
- Smoke tests must pass
- Critical sequences validated
