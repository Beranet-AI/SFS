# Project Conventions

## 1. Service Naming

- Each microservice lives under: `backend/services/<service_name>/`
- Service names are **lowercase_with_underscore**.

### backend
- Official folder:
  - Folder: `backend/`

### management
- The old name `user_management` is deprecated; we use `management` everywhere:
  - Folder: `backend/services/management/`
  - Docker service: `sfs-management`
  - Container name: `sfs-management`
  - Image: `sfs-management:latest`

### ai_decision
- The old name `ai_service` is deprecated; we use `ai_decision` everywhere:
  - Folder: `backend/services/ai_decision/`
  - Docker service: `sfs-ai_decision`
  - Container name: `sfs-ai_decision`
  - Image: `sfs-ai_decision:latest`

### data_ingestion
- The old name `decision_engine_fastapi` is deprecated; we use `data_ingestion` everywhere:
  - Folder: `backend/services/data_ingestion/`
  - Docker service: `sfs-data_ingestion`
  - Container name: `sfs-data_ingestion`
  - Image: `sfs-data_ingestion:latest`

### alerting
- Keeps the official name `alerting`:
  - Folder: `backend/services/alerting/`
  - Docker service: `sfs-alerting`
  - Container name: `sfs-alerting`
  - Image: `sfs-alerting:latest`

### frontend/webapp
- Official folder:
  - Folder: `frontend/webapp/`

### frontend/mobileapp
- Official folder:
  - Folder: `frontend/mobileapp/`

### edge
- Official folder:
  - Folder: `edge/`

### edge_controller
- The old name `device_controller` is deprecated; we use `edge_controller` everywhere:
  - Folder: `edge/edge_controller/`
  - Docker service: `sfs-edge_controller`
  - Container name: `sfs-edge_controller`
  - Image: `sfs-edge_controller:latest`



### REMOVED SERVICES (must be deleted completely)

- `alerting`
  - Folder to delete: `backend/alerting/`

- `api_gateway`
  - Folder to delete: `backend/api_gateway/`

- `api_gateway`
  - Folder to delete: `backend/services/api_gateway/`

- Temporary empty `data_ingestion`
  - Folder to delete: `backend/services/data_ingestion/` (legacy copy)

- `ai_service`
  - Folder to delete (if exists): `backend/services/ai_service/`

- `decision_engine_fastapi`
  - Folder to delete (if exists): `backend/services/decision_engine_fastapi/`

- `device_controller`
  - Folder to delete (if exists): `backend/services/device_controller/`


## 2. Python Package Structure (per service)



SmartFarm Project – Architecture & Development Conventions

(This document defines conventions and rules required for consistent development, refactoring, and long-term maintainability of the SmartFarm platform.)

1. General Architecture Principle

SmartFarm follows a modular, service-oriented architecture with clear bounded contexts, isolated deployable units, and explicit communication contracts (REST, MQTT, Event Bus).

Each service owns its domain data and logic. Shared code must be explicitly declared, version-controlled, and imported through well-defined interfaces—not implicit imports.

2. Backend Service Structure (Python)

Every backend service must follow 5 mandatory layers:

    backend/services/<service_name>/
                                domain/
                                application/
                                api/
                                infrastructure/
                                config/

| Layer          | Responsibility                                                                     |
| -------------- | ---------------------------------------------------------------------------------- |
| domain         | Business logic, entities, domain rules. No external imports (Django, FastAPI, DB). |
| application    | Use-cases, orchestration, service classes, DTO mappings.                           |
| api            | REST endpoints / serializers / input validation                                    |
| infrastructure | ORM models, repositories, DB integration, event/message adapters                   |
| config         | env loading, settings, dependency injection                                        |

Rules:
    domain must never depend on api or infrastructure
    infrastructure may depend on domain, never the opposite
    api depends on application or domain, never directly on DB

3. Folder Naming

Microservice folder names follow:

backend/services/<snake_case_name>/

backend/services/data_ingestion/
backend/services/ai_decision/
backend/services/alerting/
backend/services/management/


Avoid multi-word camelCase or uppercase names.

4. Backend Service Responsibilities (Bounded Contexts)

Management
    Authentication, roles, permissions. Token issuance and validation.

Data Ingestion
    Receive sensor events, validate, store, and publish normalized data.

AI Decision
    Consume telemetry, run ML/AI models, produce decisions, publish commands.

Alerting
    Receive decision or error events, evaluate rules, deliver notifications.

Edge Controller
    Bridge physical world (devices/sensors) with server decisions via MQTT/Modbus/etc.

Rules:

    a service must not perform logic of another service
    communication through API/MQTT/events only

5. Communication Rules

Allowed channels:

    REST (internal service API)
    MQTT topics
    Event bus messages
    WebSockets (frontend)

Forbidden:

    Direct DB access from another service
    Importing internal modules from another service
    Cross-service ORM access

6. Environment Configuration

    Each service must include:
        .env
        .env.docker
        .env.example

Rules:

    .env local only (never committed)
    .env.docker for container runtime
    .env.example is public template (required)

Service configuration is loaded only from config module

7. Environment Naming Conventions

    Management
        DJANGO_SECRET_KEY
        DJANGO_ALLOWED_HOSTS
        DJANGO_DEBUG
        POSTGRES_DB
        POSTGRES_USER
        POSTGRES_PASSWORD

    Data Ingestion
        MQTT_BROKER_URL
        MQTT_TLS_ENABLED
        POSTGRES_URL

    AI Decision
        ML_MODEL_PATH
        EVENT_BUS_URL
        DJANGO_API_BASE_URL

    Alerting
        SMTP_HOST
        SMTP_PORT
        PUSH_SERVICE_URL

    Edge Controller
        MQTT_SECURE_TLS=true
        EDGE_DEVICE_ID

8. Domain Rules

Entities must be framework-independent:

    class SensorMeasurement(Entity):
        timestamp: datetime
        temperature: float
        ammonia: float

AI, DB or MQTT imports are forbidden inside domain/.

9. Model Versioning (AI)

Model files must be stored under:
    backend/services/ai_decision/models/

File naming:
    model_<type>_v<number>.<ext>

Examples:
    model_risk_v1.pkl
    model_detection_v2.onnx

A manifest.json defines the active model:
{
  "active_model": "model_detection_v2.onnx",
  "last_updated": "2025-10-12"
}

10. Frontend Naming (Web)

Components:
    PascalCase

Files:
    <Feature>/<Component>.tsx

Environment exposed to client (only):
    NEXT_PUBLIC_*

11. Mobile App Conventions

    Same logic as web. Must consume APIs only via HTTPS.
    Requires login using management service tokens.
    Push notifications only through alerting.

12. Logging Rules

    data_ingestion/logs must include:

        received messages sample
        parsing/validation errors
        broker connectivity errors
        edge_controller must log:
        executed commands
        timestamps
        device id
        operator id (if manual command)

13. Security (required)

    All MQTT connections must support TLS.
    All REST connections must use HTTPS.
    Management controls all authentication and authorization.
    Edge devices must authenticate using keys/tokens, not anonymous connections.

14. Deployment / Runtime

    Each service runs in its own container.
    Containers never share volume for application code.

    Communication only through network.
    No direct container-to-container filesystem access.

15. Refactor Policy

A refactor is approved only if:
    service boundaries preserved
    domain logic isolated
    CI passes
    no cross-service coupling introduced
    .env.example is updated

Summary by One Sentence Each
    data_ingestion → system gateway for sensor input
    ai_decision → analytical brain
    edge_controller → actuator and device bridge
    management → authentication and authorization
    alerting → notifications for humans
    frontend/webapp → full dashboard
    frontend/mobileapp → field interaction UI


(This convention file is mandatory and must be followed for all future development, refactoring, and deployment activities.)

# Project Architecture Overview

1. Folder Responsibilities

    domain/:
        Contains pure business logic
        No external dependencies (no Django, DRF, FastAPI, etc.)
        Defines core Entities, ValueObjects, Services, and Interfaces
        Example: domain/alerts/entities.py → Alert, domain/devices/services.py

    infrastructure/:
        Deals with side-effects and external systems
        Includes:
        ORM models (...Model) in infrastructure/db/models.py
        Repositories that implement interfaces
        API clients (e.g., MQTT, sensors, external services)
        Implements domain interfaces (e.g., repositories)
    api/:
        Only does HTTP <-> application/domain mapping
        Uses Django/FastAPI/DRF
        No business logic here

    Views/controllers must delegate to use-cases/services in application/ or domain/

2. Naming Conventions

    Domain Entities: Sensor, Alert, Device
    Located in: domain/entities.py or domain/<context>/entities.py
    ORM Models: SensorModel, DeviceModel
    Located in: infrastructure/db/models.py
    DTOs / Serializers: SensorDTO, AlertSerializer

3. Frontend Naming (React / Next.js)

    React components: PascalCase
    Example: SensorCard.tsx, AlertBanner.tsx
    Hooks: useSomething
    Example: useAlertFetcher
    Env variables: Prefix with NEXT_PUBLIC_ for frontend usage

4. Coding Standards

    Python:
        Follow PEP8
        Enforced with Black + Pylint

    JS/TS:
        Enforced with ESLint + Prettier

5. Controllers/Vews

    Views/controllers must be thin and delegate all logic to services or use cases.