# Audit Logging

Audit logging ensures accountability and traceability.

---

## What Is Audited

- Incident creation, acknowledgement, resolution
- Health state transitions
- User authentication events
- Device and edge registration

---

## Audit Log Contents

Each audit entry includes:
- Timestamp
- Actor (user/service/edge)
- Action performed
- Target entity (type + id)
- Correlation ID

---

## Audit Log Storage

- Stored in Management database
- Append-only semantics
- Never modified or deleted

---

## Access Control

- Audit logs are read-only
- Accessible to Admin role only
- Not exposed to frontend by default

---

## Operational Use

- Incident investigation
- Security reviews
- Compliance reporting
