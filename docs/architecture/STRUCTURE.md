# SmartFarm Project Structure

This repository is organized to match the proposed layered architecture for the SmartFarm IoT platform. Each directory is scoped to a specific concern so backend, edge, and frontend teams can work independently without mixing artifacts.

## Edge layer
- `edge/labview_modules/` – LabVIEW integrations for on-premise controllers.
- `edge/configs/` – Device and gateway configuration files (.gitkeep placeholder).
- `edge/logs/` – Runtime logs captured from edge gateways (.gitkeep placeholder).

## Backend services
<<<<<<< HEAD
- `backend/services/user_management/` – Django stack (farms, barns, zones, sensors).
- `backend/services/decision_engine_fastapi/` – FastAPI decision/ingestion gateway that forwards readings to Django.
- `backend/services/data_ingestion/` – Ingestion scaffold; `logs/` reserved for broker/ingestion logs.
- `backend/services/device_controller/` – Device control service scaffold.
- `backend/services/alerting/` – Alerting service scope (FastAPI scaffold + Django alert app/code).
=======
- `backend/services/user_management/` – Django stack (farms, barns, zones, sensors, alerts).
- `backend/services/decision_engine_fastapi/` – FastAPI decision/ingestion gateway that forwards readings to Django.
- `backend/services/data_ingestion/` – Ingestion scaffold; `logs/` reserved for broker/ingestion logs.
- `backend/services/device_controller/` – Device control service scaffold.
- `backend/services/alerting/` – Alert delivery scaffold.
>>>>>>> main
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
- `infrastructure/docker/` – Docker Compose stacks and Docker assets (.gitkeep placeholder).
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
<<<<<<< HEAD
- Existing service code has **not** been relocated to avoid breaking imports; use the aliases above when adding new modules to stay consistent with the proposed architecture. The alerting app has been moved into `backend/services/alerting/` to better match the service boundary.
=======
- Existing service code has **not** been relocated to avoid breaking imports; use the aliases above when adding new modules to stay consistent with the proposed architecture.
>>>>>>> main
