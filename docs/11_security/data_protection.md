# Data Protection

This document describes how SFS protects data at rest and in transit.

---

## Data in Transit

- All external communication via HTTPS
- Internal service calls over isolated Docker network
- No plaintext credentials in URLs or logs

---

## Data at Rest

- PostgreSQL stores all persistent data
- Database access restricted to Management service
- Backups encrypted at rest (planned)

---

## Sensitive Data Handling

- Passwords stored as salted hashes
- Tokens stored securely (not logged)
- Personally identifiable data minimized

---

## Data Minimization

- Frontend receives only necessary fields
- Telemetry data exposed only via controlled APIs
- Health and incident data filtered by role

---

## Compliance Considerations

- Data retention policies enforced
- Deletion operations audited
- Export operations logged
