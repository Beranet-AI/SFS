# Authentication & Authorization

---

## Authentication (AuthN)

### User Authentication
- JWT-based authentication
- Access Token (short-lived)
- Refresh Token (long-lived)

Endpoints:
- POST /api/v1/auth/login/
- POST /api/v1/auth/refresh/

---

### Service Authentication
- Static service tokens
- Tokens scoped per service
- Tokens rotated manually (initially)

---

### Edge Authentication
- API key per edge node
- Key associated with edge identity
- Keys stored hashed

---

## Authorization (AuthZ)

### Role-Based Access Control (RBAC)

Roles:
- Admin
- Operator
- Viewer

Permissions:
- View livestock and telemetry
- Manage incidents
- Manage devices (Admin only)

---

## Enforcement Points

- API layer enforces permissions
- No permission checks in UI
- No permission bypass in FastAPI services

---

## Security Rules

- Anonymous write operations are forbidden
- Incident state transitions require authentication
- Edge APIs accept only edge credentials
