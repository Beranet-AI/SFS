# System Architecture – Baseline (Today)

This repository is organized to match the proposed layered architecture for the SmartFarm IoT platform. Each directory is scoped to a specific concern so backend, edge, and frontend teams can work independently without mixing artifacts.

## Edge layer
- `edge/labview_modules/` – LabVIEW integrations for on-premise controllers.
- `edge/configs/` – Device and gateway configuration files (.gitkeep placeholder).
- `edge/logs/` – Runtime logs captured from edge gateways (.gitkeep placeholder).

## Backend services
- `backend/alerting/` - other service
- `backend/services/management/` – Django stack (farms, barns, zones, sensors).
- `backend/services/decision_engine_fastapi/` – FastAPI decision/ingestion gateway that forwards readings to Django.
- `backend/services/data_ingestion/` – Ingestion scaffold; `logs/` reserved for broker/ingestion logs.
- `backend/services/device_controller/` – Device control service scaffold.
- `backend/services/alerting/` – Alerting service scope (FastAPI scaffold + Django alert app/code).
- `backend/services/ai_service/` – AI/analytics microservice (aligns with the planned `ai_decision` role); `models/` and `notebooks/` capture ML assets.
- `backend/services/api_gateway/` – API gateway façade (current implementation lives here; a mirror directory `backend/api_gateway/` is provided for tooling that expects the top-level path).

### Domain contracts
- `backend/domain/` – Shared domain models and interfaces for services that need a common contract.

## API gateway (alias)
- `backend/api_gateway/` – Placeholder alias pointing to the gateway service scope. Place new gateway configs/docs here if tooling assumes a top-level path.

## Frontend
- `frontend/webapp/` – Next.js dashboard.
- `frontend/mobileapp/` – Reserved for a future mobile client scaffold.

## Infrastructure & ops
- `infrastructure/docker/` – Docker Compose stacks and Docker assets (primary `docker-compose.yml` lives here).
- `infrastructure/k8s/` – Kubernetes/Helm manifests (.gitkeep placeholder).
- `infrastructure/mqtt_broker/` – MQTT broker configuration (.gitkeep placeholder).

## Data & logs
- `data/sensor_data/` – Raw sensor payloads for replay/testing.
- `data/processed_data/` – Derived/cleaned datasets.
- `logs/system/` – Centralized system/application logs.

## Configuration
- `configs/global/` – Shared environment configuration, secrets templates, and tuning files.

## Tests
- `tests/unit/` – Service-level unit tests.
- `tests/integration/` – Cross-service integration and end-to-end tests.

## Notes
- Empty directories contain `.gitkeep` to keep the structure visible in Git until assets are added.

- Existing service code has **not** been relocated to avoid breaking imports; use the aliases above when adding new modules to stay consistent with the proposed architecture. The alerting app has been moved into `backend/services/alerting/` to better match the service boundary.


## 2. Current Folder Structure (High-Level)

```text
root/
  backend/
    alerting/
        alerts/
    api_gateway/
    domain/
        entities/
    services/
        ai_service/
            api/
            application/
            domain/
            entities/
            infrastructure/
            models/
            notebooks/
        alerting/
            alerts/
                migrations/
            api/
                routes/
                schemas/
            app/
                /domain
                services/
            application/
            domain/
            entities/
            infrastructure/
                core/
                db/
            models/
            tests/
        api_gateway
            api/
                routes/
                schemas/
            application/
            domain/
            entities/
            infrastructure/
                core/
                db/
            models/
            tests/
        data_ingestion
            api/
                routes/
                schemas/
            app
                domain/
                service/
            application/
            domain/
            entities/
            infrastructure/
                core/
                db/
            logs/
            models/
            tests/
        decision_engine_fastapi
            api/
            application/
            domain/
            entities/
            infrastructure/
            models/
        device_control
            api/
                routes/
                schemas/
            application/
            domain/
            entities/
            infrastructure/
                core/
                db/
            logs/
            models/
            tests/
        management/
            alerts/
                migrations/
            api/
                management/
                    commands/
            application/
                alerts/
            config/
            devices/
                migrations/
            domain/
            entities/
            farm/
                migrations/
            health/
                migrations/
            infrastructure/
            livestock/
                migrations/
            telemetry/
                migrations/
        user_management/
    configs/
        global/
    data/
        processed_data/
        sensor_data/
    docs/
        architecture/
    edge/
        configs/
        labview_modules/
        logs/
    frontend/
        mobileapp/
        webapp/
            .next/
                dev/
            node_modules/
            public/
            src/
                app/
                components/
                lib/
    infrastructure/
        docker/
        k8s/
        mqtt_broker/
    logs
    tests/
        integratin/
        unit/
    venv/
        include/
        lib/
        scripts/
  
  ...


## 3. Current Logical Layers

Domain Layer (domain/)

    Contains pure business logic.
    No dependency on Django, DRF, FastAPI, or any framework.

    Defines:

        Entities (e.g., Sensor, Device, Alert)
        Value Objects (e.g., Temperature, ThresholdRange)
        Interfaces (e.g., SensorRepository, AlertService)
        Business Rules / Policies

Application Layer (optional or embedded within domain)

    (If exists) Coordinates use cases or services.
    Orchestrates interactions between entities and infrastructure.
    Thin services may exist here (e.g., CreateAlertRuleUseCase).

Infrastructure Layer (infrastructure/)

    Handles side effects and integration:

        ORM models (SensorModel, DeviceModel)
        Repository implementations
        External APIs (e.g., MQTT, hardware sensors)
        Maps to domain interfaces

API Layer (api/)

    Maps HTTP endpoints to domain or application logic.
    Uses FastAPI / DRF / Django Views.
    No business logic – only parses request, delegates, and returns response.

Frontend Layer (frontend/webapp)

    Built with React + Next.js

    Organized with:

        Components (SensorCard.tsx, AlertBanner.tsx)
        Hooks (useLatestReadings, useAlerts)
        Uses SWR for data fetching
        Respects domain-driven naming and clean separation of concerns
        Env config via NEXT_PUBLIC_... variables

## 4. Architecture Observations


    ✅ Clean separation of concerns:

        Domain logic is pure and testable.
        Side effects isolated in infrastructure.
        HTTP logic in API layer only.

    ✅ Hexagonal Architecture Principles respected.

    ✅ Naming conventions are consistent and align with domain language.

    ✅ Frontend uses declarative and modern practices (SWR, Tailwind, modular components).

    ⚠️ Application layer (use cases/services) might be thin or missing in places; some coordination logic may exist in views instead.

    ⚠️ Tight coupling between API layer and data layer in a few endpoints (e.g., direct queryset filtering).

    ✅ Dev tooling in place: Docker, Docker Compose, ESLint, Prettier, Black, Pylint.

## 5. Known Issues and Technical Debt

    ❌ Service token errors:

        403 Invalid service token errors occur in frontend when calling Django APIs.
        Likely due to token mismatch or FastAPI not injecting Authorization headers correctly.

    ❌ FastAPI service sometimes fails to start:

        Intermittent startup failures, possibly due to Docker dependency race conditions or port conflicts (e.g., database/migration order).

    ⚠️ Alert system still under-integrated:

        Alert rules are defined but not fully enforced.
        No visual/UI feedback or log entries on threshold breach.

    ⚠️ UI does not refresh or reflect new sensors immediately:

        New sensors are not shown until manual reload.
        Likely due to SWR caching or lack of mutate/revalidation triggers post-creation.

    ⚠️ Business logic leaked into views:

        Some Django views directly perform filtering or orchestration logic.
        These responsibilities should be moved to domain services or use cases.

    ❌ Error boundaries not implemented in frontend:

        Network or server-side errors (403, 500) result in broken UI without fallback UI or recovery mechanism.

    ⚠️ Missing automated test coverage:

        Lack of unit tests for domain logic and integration tests for API/infra.
        Frontend components and hooks also lack test coverage.

    ⚠️ Poor separation and categorization of files:

        domain logic is mixed with views/models
        some services share config/env inconsistently
        naming of services/containers is not consistent (e.g. , user_management vs management)
        .env files are scattered and sometimes duplicated.
        Files are not consistently organized based on architectural boundaries.
        Some infrastructure logic resides inside api/, and domain entities are mixed with serializers or models.
        Refactoring is needed to cleanly split code into domain/, infrastructure/, and api/

## 6. Domain Map – Bounded Contexts & Services

    این سند مرزهای دامنه‌ای سیستم SmartFarm را تعریف می‌کند. هدف از این مرزبندی، جداسازی مسئولیت‌ها و ساده‌سازی نگه‌داری و توسعه‌پذیری است.

    ---

    ## 1. User & Access Management
    - **Service:** `management` (Django)
    - **Responsibilities:**
    - User accounts and registration
    - Role-based permissions (e.g., farmer, admin, technician)
    - JWT & token-based authentication
    - Internal service tokens and validations

    ---

    ## 2. Farm Structure & Configuration
    - **Service:** `management` (Django)
    - **Responsibilities:**
    - Define farm → barns → zones hierarchy
    - Assign sensors to specific zones or barns
    - Maintain metadata for farms, devices, and zones
    - Serve structured farm hierarchy to UI

    ---

    ## 3. Sensor Data & Telemetry
    - **Service:** `data_ingestion` (FastAPI)
    - **Responsibilities:**
    - Receive and validate raw telemetry from sensors (e.g., MQTT, HTTP)
    - Normalize and store readings
    - Enrich sensor data (timestamps, farm linkage, etc.)
    - Push data to FastAPI decision engine

    ---

    ## 4. Decision Making & AI Inference
    - **Service:** `ai_decision` (FastAPI)
    - **Responsibilities:**
    - Load ML models and rules
    - Make binary/continuous decisions based on sensor inputs
    - Support configurable thresholds (`DECISION_THRESHOLD`)
    - Serve decision results to UI or downstream services

    ---

    ## 5. Alerting & Notification System
    - **Service:** `alerting` (FastAPI)
    - **Responsibilities:**
    - Manage AlertRules and thresholds
    - Trigger alerts when new data violates thresholds
    - Maintain list of active alerts
    - Log alerts and optionally notify UI / logging service

    ---

    ## 6. Frontend UI
    - **Service:** `webapp`
    - **Tech Stack:** Next.js + TypeScript
    - **Responsibilities:**
    - Interactive dashboard for sensor data and alerts
    - Real-time UI updates (via polling or SWR)
    - View & manage farm structure
    - Display alert banners and sensor conditions
    - Token-based auth (optional session persistence)

    ---

    ## 7. Mobile App (Optional / Future)
    - **Service:** `mobileapp`
    - **Tech Stack:** React Native
    - **Responsibilities:**
    - View farm status and alerts
    - Simple control interface for devices
    - Offline cache and sync
    - Push notifications for alerts

    ---

    ## 8. Edge Controller
    - **Service:** `edge_controller` (FastAPI)
    - **Responsibilities:**
    - Run on edge devices (e.g., Raspberry Pi)
    - Interface with local sensors
    - Send data upstream to `data_ingestion`
    - Perform failover logic in case of disconnection
    - Bridge between hardware and cloud
    - Issue control commands (e.g., turn on fan/pump)
    - Communicate with physical devices or emulators
    - Log actuator activities
    - (Optionally) expose current device states

    ---

💡 این فایل به‌صورت زنده نگه‌داری شود و در صورت اضافه‌شدن سرویس، زمینه یا تغییر مسئولیت‌ها، به‌روز گردد.
