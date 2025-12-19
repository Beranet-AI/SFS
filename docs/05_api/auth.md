
---

# 🔐 Auth API

## `docs/05_api/auth.md`

```md
# Authentication & Authorization

---

## Authentication Model

- JWT-based authentication
- Access Token (short-lived)
- Refresh Token (long-lived)

---

## Endpoints

### POST /api/v1/auth/login/
Authenticates user and returns tokens.

### POST /api/v1/auth/refresh/
Refreshes access token.

---

## Authorization

- Role-based access control (RBAC)
- Permissions enforced at API layer
- Service-to-service calls use static tokens

---

## Security Rules

- No anonymous write operations
- All incidents actions require authentication
- Edge APIs use API keys
