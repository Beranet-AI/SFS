# SmartFarm System – DDD-Guided Microservices Redesign

This document refines the microservices architecture using Domain-Driven Design (DDD) bounded contexts tailored to the current repository layout.

## 1) Domain and Subdomain Breakdown
- **Core domain:** Farm operations intelligence (sensor telemetry → decisions/alerts → device control). 
- **Supporting domains:** Identity & access, farm master data (farms/barns/zones/animals), device registry, rule management, alert lifecycle, data ingestion.
- **Generic domains:** API gateway, shared observability/security, reporting/analytics enablement.

### Subdomains (inferred from code and folders)
- **Identity & Access:** Django `api/permissions.py`, middleware, auth settings in `backend/services/management`.
- **Farm Registry:** Django apps `farm`, `livestock`, `devices` storing farms, barns, livestock, devices, tags.
- **Telemetry Ingestion:** FastAPI services `data_ingestion`, `decision_engine_fastapi` handling sensor inputs and pipeline hand-off.
- **Rule Engine & Alerts:** FastAPI `monitoring`, decision logic in `decision_engine_fastapi` for evaluating conditions and emitting alerts.
- **Device Control:** FastAPI `device_controller` coordinating commands to edge devices.
- **Analytics/AI:** `ai_service` notebooks/models consuming curated data.
- **Gateway:** `backend/services/api_gateway` providing facade.

## 2) Bounded Contexts & Context Map
- **Identity & Access BC:** Authentication, authorization, tenant/farm membership. Upstream to all internal services (customer-supplier for auth tokens). Implemented by the Django management service.
- **Farm Management BC:** Farm/barn/zone/animal/tag registries; owns lifecycle and IDs. Supplies references to other contexts (upstream supplier; others are conformist). Implemented by Django farm/livestock/apps.
- **Device Registry BC:** Device + sensor inventory and status. Depends on Farm Management for farm/barn/zone identities. Consumed by Ingestion and Device Control. Implemented by Django `devices` app (future dedicated service).
- **Telemetry Ingestion BC:** Receives raw sensor/device payloads, validates against Device Registry, publishes canonical `telemetry.reading.ingested` events. Downstream consumers: Decision & Alerts, Analytics. Implemented by FastAPI `data_ingestion`.
- **Decision & Alerts BC:** Maintains alert rules, evaluates telemetry, raises/resolves alerts, publishes `alert.raised`/`alert.resolved` events, requests actuation. Implemented by FastAPI `monitoring` + `decision_engine_fastapi` (to merge).
- **Device Control BC:** Executes actuation commands; subscribes to decision events/commands; tracks command outcomes. Implemented by FastAPI `device_controller`.
- **Analytics/AI BC:** Consumes curated telemetry/alerts for insight and models; exposes inference jobs/APIs. Implemented by `ai_service`.
- **API Gateway BC:** Public entrypoint; routes to internal services; enforces authN/Z and rate limits. Implemented by FastAPI gateway.

### Textual Context Map
- Gateway → Identity (auth) and routes to Farm Management, Device Registry, Telemetry Ingestion, Decision & Alerts, Analytics.
- Telemetry Ingestion → publishes telemetry events; depends on Device Registry for validation.
- Decision & Alerts ← consumes telemetry events; → publishes alert events; → sends commands to Device Control.
- Device Control ← receives commands from Decision & Alerts; → emits command status events.
- Analytics/AI ← consumes telemetry and alerts; may expose results to Gateway.
- Identity → supplies tokens/claims to Gateway and services.

## 3) Bounded Context Responsibilities (Service/Table Mapping)
| Bounded Context | Responsibility | Service | Database | Depends on |
| --- | --- | --- | --- | --- |
| Identity & Access | Users, roles, permissions, tokens | management (Django) | Postgres `identity` | – |
| Farm Management | Farms, barns, zones, animals, tags | management/farm & livestock apps (→ future farm service) | Postgres `farm_mgmt` | Identity |
| Device Registry | Devices, sensors, status, assignments | management/devices (→ future device service) | Postgres `device_registry` | Farm Management, Identity |
| Telemetry Ingestion | Device enrollment, telemetry intake, schema validation | data_ingestion (FastAPI) | Time-series/queue + Postgres `ingestion` | Device Registry |
| Decision & Alerts | Rules, thresholds, alert lifecycle | monitoring + decision_engine_fastapi (merge) | Postgres `alerts` | Telemetry events, Farm/Device references |
| Device Control | Actuation commands, feedback | device_controller | Postgres `device_control` | Decision & Alerts, Device Registry |
| Analytics/AI | Feature pipelines, inference endpoints | ai_service | Object store + Postgres `ai` | Telemetry, Alerts |
| API Gateway | Routing, auth, rate-limits, observability | api_gateway | N/A (config only) | Identity |

## 4) New Microservice Layout & Contracts
Services (each owns its DB schema):
1. **identity-service** (Django/DRF): Auth, tenants, RBAC, token issuance.
   - REST: `POST /auth/login`, `POST /auth/refresh`, `GET /users/me`, `POST /users`, `GET /roles`.
   - Events: publishes `identity.user.created`, `identity.role.assigned`.
2. **farm-service** (Django/DRF): Farms, barns, zones, animals, RFID tags.
   - REST: `POST/GET/PATCH /farms`, `/barns`, `/zones`, `/animals`, `/tags/assign`.
   - Events: publishes `farm.zone.updated`, `farm.animal.moved`.
3. **device-registry-service** (FastAPI): Devices, sensors, status.
   - REST: `POST/GET /devices`, `/devices/{id}/status`, `POST /sensors`.
   - Events: publishes `device.registered`, `device.status.changed`.
4. **ingestion-service** (FastAPI + MQTT/HTTP): Accepts raw payloads, validates, stores canonical readings.
   - REST: `POST /ingest/http`, `POST /ingest/bulk`.
   - MQTT: `/devices/{id}/telemetry`.
   - Events: publishes `telemetry.reading.ingested` (sensor_id, value, ts, quality).
5. **decision-alerts-service** (FastAPI): Rules, evaluation, alert lifecycle.
   - REST: `POST/GET /rules`, `POST /rules/{id}/toggle`, `GET /alerts`, `POST /alerts/{id}/ack`, `POST /alerts/{id}/resolve`.
   - Events: subscribes `telemetry.reading.ingested`; publishes `alert.raised`, `alert.resolved`, `actuation.command.requested`.
6. **device-control-service** (FastAPI): Executes actuation commands.
   - REST: `POST /commands`, `GET /commands/{id}`.
   - Events: subscribes `actuation.command.requested`; publishes `actuation.command.executed`.
7. **analytics-service** (FastAPI): Feature extraction, inference endpoints.
   - REST: `POST /inference`, `GET /models`, `POST /training-jobs`.
   - Events: subscribes telemetry/alert streams; publishes `analytics.anomaly.detected`.
8. **api-gateway** (FastAPI/NGINX alternative): Public interface; validates JWT, routes to services; exposes OpenAPI.

## 5) Aggregates & Data Ownership
- **Identity:** Aggregate roots `User`, `Role`, `Permission`, `Tenant`. Owned by identity-service.
- **Farm Management:** Aggregates `Farm` → `Barn` → `Zone`; `Animal` with `RfidTag`. Owned by farm-service; other contexts reference by IDs only.
- **Device Registry:** Aggregate `Device` with `Sensor` and `SensorType`; status history as value objects. Owned by device-registry-service.
- **Telemetry:** Aggregate `SensorReading` (root) referencing `Sensor` ID, timestamp, value, quality, raw payload; owned by ingestion-service. Downstream consumers use events, not joins.
- **Rules/Alerts:** Aggregates `AlertRule` (root) and `Alert` (root). Decision service owns rule storage and alert lifecycle.
- **Actuation:** Aggregate `Command` with `CommandResult`. Device-control owns execution state.
- **Analytics:** Aggregates `ModelArtifact`, `InferenceJob`. Analytics service owns derived data.

### Data Ownership Matrix
- Identity tables → identity-service only.
- Farm/Animal/Tag tables → farm-service only; foreign keys are internal; other services use IDs received via APIs/events.
- Device/Sensor tables → device-registry-service only.
- Telemetry readings → ingestion-service (time-series/warehouse), exposed via API for consumers.
- Rules/Alerts → decision-alerts-service.
- Commands → device-control-service.
- Models/Jobs → analytics-service.

## 6) Repository Structure Proposal
```
services/
  identity-service/
    domain/ application/ infrastructure/ interfaces/api/
  farm-service/
  device-registry-service/
  ingestion-service/
  decision-alerts-service/
  device-control-service/
  analytics-service/
  api-gateway/
shared-kernel/
  domain/events/
  libraries/auth/, observability/
frontend/
edge/
infrastructure/
  docker/
  k8s/
configs/
  env/
  secrets-templates/
docs/
tests/
```

### New Folder Tree (high level)
```
services/
  identity-service/
  farm-service/
  device-registry-service/
  ingestion-service/
  decision-alerts-service/
  device-control-service/
  analytics-service/
  api-gateway/
shared-kernel/
  domain/
  libraries/
frontend/
edge/
infrastructure/
  docker/
  k8s/
configs/
docs/
tests/
```

### Mapping Table (old → new)
| Current Path | New Path | Notes |
| --- | --- | --- |
| `backend/services/management/api/` | `services/identity-service/interfaces/api/rest/` | Auth + user endpoints. |
| `backend/services/management/config/` | `services/identity-service/interfaces/api/django_config/` | Settings + middleware. |
| `backend/services/management/farm/` | `services/farm-service/interfaces/api/rest/` | Farm CRUD splits into dedicated service. |
| `backend/services/management/livestock/` | `services/farm-service/interfaces/api/rest/` | Animal lifecycle and tagging. |
| `backend/services/management/devices/` | `services/device-registry-service/interfaces/api/rest/` | Device/sensor registry APIs. |
| `backend/services/data_ingestion/` | `services/ingestion-service/` | Telemetry intake HTTP/MQTT adapters. |
| `backend/services/decision_engine_fastapi/` | `services/decision-alerts-service/` | Merge with monitoring for rule evaluation. |
| `backend/services/monitoring/` | `services/decision-alerts-service/` | Live status stream (derived telemetry). |
| `backend/services/device_controller/` | `services/device-control-service/` | Actuation commands + results. |
| `backend/services/api_gateway/` | `services/api-gateway/` | Public ingress and routing. |
| `backend/services/ai_service/` | `services/analytics-service/` | Model training/inference endpoints. |
| `backend/domain/entities/` | `shared-kernel/domain/entities/` | Shared value objects/identifiers. |
| `backend/domain/models.py` | `shared-kernel/domain/__init__.py` | Backwards-compatible re-exports only. |
| `frontend/` | `frontend/` (unchanged) | Consumes gateway APIs; stay separate package. |
| `infrastructure/docker/` | `infrastructure/docker/` (unchanged) | Compose/K8s overlays stay grouped. |
| `edge/` | `edge/` (unchanged) | Edge agent remains isolated. |
| `configs/` | `configs/` (unchanged) | Cross-service configs/templates. |
| `logs/` | `infrastructure/archive/logs/` | Archive runtime logs outside source tree. |
| `data/` | `infrastructure/archive/data/` | Move sample data away from runtime paths. |
| `tests/` | `tests/` (unchanged) | Host integration/system tests spanning services. |

### Path Mapping (old → new)
- `backend/services/management/config/*` → `services/identity-service/interfaces/api/django_config/`
- `backend/services/management/api/*` → `services/identity-service/interfaces/api/rest/`
- `backend/services/management/farm/*` → `services/farm-service/interfaces/api/rest/`
- `backend/services/management/livestock/*` → `services/farm-service/interfaces/api/rest/`
- `backend/services/management/devices/*` → `services/device-registry-service/interfaces/api/rest/`
- `backend/services/monitoring/*` + `backend/services/decision_engine_fastapi/*` → `services/decision-alerts-service/`
- `backend/services/device_controller/*` → `services/device-control-service/`
- `backend/services/data_ingestion/*` → `services/ingestion-service/`
- `backend/services/api_gateway/*` → `services/api-gateway/`
- `backend/services/ai_service/*` → `services/analytics-service/`
- `backend/domain/entities/*` → `shared-kernel/domain/entities/`
- `backend/domain/models.py` (shim) → `shared-kernel/domain/__init__.py` (re-export or deprecated notice)
- Legacy `logs/`, `data/`, SQLite artifacts → archive/remove under `infrastructure/archive/` during migration.

## 7) Communication & Auth Design
- **Gateway-first:** All external traffic via api-gateway; internal services on a private network. 
- **Sync HTTP:** Gateway → services via REST; services may call each other only via internal REST or message bus if unavoidable.
- **Async Events:** Central message bus (Kafka/Redis Streams/NATS). Event contracts: 
  - `telemetry.reading.ingested`, `alert.raised`, `alert.resolved`, `actuation.command.requested`, `actuation.command.executed`, `analytics.anomaly.detected`, `identity.user.created`.
- **Tokens:**
  - External JWT (short-lived) issued by identity-service; validated by gateway.
  - Internal service-to-service JWT with audience = service name, signed by identity-service; rotated via JWKS.
  - Separate scopes for read/write; no database-level cross access.
- **API Separation:** `/public` endpoints through gateway; `/internal` endpoints protected with mutual TLS + internal JWT.

## 8) Docker, Env, CI/CD, Monorepo
- **Docker:** Per-service multi-stage builds (builder + runtime), slim Python base (e.g., `python:3.11-slim`), non-root user, dependency caching via `pip install --no-cache-dir` with wheels cache.
- **Compose:** Define isolated networks: `public` (gateway) and `services`; each service exposes only internal ports; gateway publishes external port 80/443; volumes only for persistent data and minimal bind mounts. Remove shared `.env` in favor of per-service `.env.docker` templates.
- **Env/Secrets:** `.env.example` per service; use Docker secrets/K8s secrets; store prod secrets in Vault/GitHub Actions secrets; rotate signing keys; avoid committing SQLite/db files (`management/db.sqlite3`).
- **CI/CD:** GitHub Actions matrix per service: lint (ruff/flake8, mypy), test, build image, scan (Trivy/Snyk), push to registry; compose smoke tests; dependency updates via Dependabot; secret scanning (Gitleaks); IaC scanning for `infrastructure/`.
- **Monorepo:** Keep monorepo but enforce service boundaries under `services/`; shared-kernel packages versioned internally; use tools like `poetry`/`pip-tools` or `npm workspaces` per service.

## 9) Migration Plan
**Phase 1 – Preparation**
- Create `services/` structure and `shared-kernel/` with domain entities as a Python package; add per-service requirements and Docker templates. Risk: import breakage—mitigate with compatibility shims. Tests: unit import smoke tests.

**Phase 2 – Identity & Farm split**
- Move Django `api`, `farm`, `livestock`, `devices` into separate `identity-service`, `farm-service`, `device-registry-service` apps; update settings and URLs; adjust db migrations to new schemas. Risk: migrations divergence; mitigate with feature toggles and dual-write if needed. Tests: Django migrations, auth flows, CRUD APIs.

**Phase 3 – Ingestion & Alerts consolidation**
- Merge `monitoring` and `decision_engine_fastapi` into `decision-alerts-service`; refactor ingestion endpoints to publish events to bus; adjust consumers. Risk: event schema drift; mitigate with schema registry and consumer contracts. Tests: integration tests for telemetry-to-alert path.

**Phase 4 – Device Control & Analytics isolation**
- Isolate actuation logic in device-control-service; move AI notebooks/models to analytics-service with APIs. Risk: model dependency size; mitigate with build caching and artifact storage. Tests: command execution mocks, model inference smoke tests.

**Phase 5 – Gateway enforcement**
- Route all external traffic through api-gateway; enforce JWT validation; add rate limiting and observability (OpenTelemetry). Risk: latency; mitigate with caching and circuit breakers. Tests: gateway e2e routing and auth.

**Phase 6 – Data & Events hardening**
- Enforce database-per-service; remove cross-service DB access; implement message bus and contracts; add outbox pattern for telemetry and alerts. Risk: eventual consistency; mitigate with retries and idempotency keys. Tests: reliability and idempotency scenarios.

**Phase 7 – CI/CD and Ops**
- Implement per-service pipelines, security scans, container hardening; set up monitoring/logging; finalize vault-based secrets. Risk: pipeline complexity; mitigate with reusable workflow templates. Tests: pipeline dry-runs.
