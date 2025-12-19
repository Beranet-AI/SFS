# Threat Model

This document identifies and mitigates security threats in SFS
using a STRIDE-inspired approach.

---

## Assets

- Livestock health data
- Incident records
- Telemetry streams
- User credentials
- Edge node identities

---

## Trust Boundaries

1. Internet ↔ WebApp
2. WebApp ↔ Backend APIs
3. Edge Network ↔ Edge Controller
4. Internal Service-to-Service calls
5. Persistent Data Store (PostgreSQL)

---

## Threat Categories & Mitigations

### Spoofing
Threat:
- Impersonation of users or edge nodes

Mitigations:
- JWT authentication for users
- API keys for edge nodes
- Service tokens for internal calls

---

### Tampering
Threat:
- Modification of telemetry or incidents

Mitigations:
- HTTPS everywhere
- Immutable telemetry storage
- Explicit incident state transitions

---

### Repudiation
Threat:
- Denial of performed actions

Mitigations:
- Audit logs for all state changes
- Correlation IDs per request

---

### Information Disclosure
Threat:
- Unauthorized access to sensitive data

Mitigations:
- RBAC enforcement
- DTO-based responses (no raw models)
- No direct DB access outside Management

---

### Denial of Service
Threat:
- Telemetry flooding
- API abuse

Mitigations:
- Rate limiting (planned)
- Stateless service scaling
- Edge-side preprocessing

---

### Elevation of Privilege
Threat:
- Gaining higher permissions

Mitigations:
- Role-based permissions
- No implicit admin privileges
- Explicit permission checks
