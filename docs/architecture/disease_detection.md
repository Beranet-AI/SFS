# AI-Based Livestock Disease Detection (Mastitis-first)

This document describes how to integrate AI-driven disease detection—starting with mastitis—into the SmartFarm system without breaking the current multi-layer architecture (LabVIEW → FastAPI → Django → Node.js dashboard).

## Data Model Extensions (Django)
Field-level tables are introduced in the new `health` app to keep disease data isolated while reusing existing farm/livestock registries.

### `health_cows` (table: `cows`)
- `id` (PK)
- `animal_id` (FK → `livestock_animal`, unique)
- `lactation_stage` (char: early/mid/late/dry)
- `parity` (int, #calvings)
- `days_in_milk` (int, nullable)
- `last_calving_date` (date, nullable)
- `created_at`, `updated_at`

### `health_diseases` (table: `diseases`)
- `id` (PK)
- `code` (unique), `name`
- `description`
- `symptoms` (JSON array)
- `detection_methods` (JSON array)
- timestamps

### `health_ml_models` (table: `ml_models`)
- `id` (PK)
- `name`, `version`
- `disease_id` (FK → `diseases`)
- `framework` (sklearn/pytorch/onnx/etc.)
- `artifact_path` (URI to model binary)
- `input_schema` (JSON feature spec)
- `metrics` (JSON: AUC/F1/precision/recall)
- `is_active` (bool)
- timestamps

### `health_sensor_data` (table: `sensor_data`)
- `id` (PK)
- `sensor_id` (FK → `devices_sensor`)
- `sensor_type_id` (FK → `devices_sensortype`)
- `cow_id` (FK → `cows`, nullable for ambient sensors)
- `ts` (datetime, indexed)
- `value`, `unit`, `quality`, `raw_payload`
- `created_at`

### `health_predictions` (table: `predictions`)
- `id` (PK)
- `model_id` (FK → `ml_models`)
- `disease_id` (FK → `diseases`)
- `cow_id` (FK → `cows`)
- `status` (`healthy|suspected|at_risk`)
- `probability` (decimal)
- `predicted_at` (datetime, indexed)
- `features` (JSON feature vector)
- `feature_window_start`, `feature_window_end`

### `health_disease_records` (table: `disease_records`)
- `id` (PK)
- `cow_id` (FK → `cows`)
- `disease_id` (FK → `diseases`)
- `status` (`suspected|confirmed|recovered`)
- `source_prediction_id` (FK → `predictions`, nullable)
- `diagnosed_at`, `resolved_at`
- `notes`

## Recommended Microservice Placement
- **Inference microservice (FastAPI)** under `backend/services/ai_service`:
  - Receives pre-processed sensor windows and returns predictions.
  - Uses model registry (`ml_models`) for loading artifacts and metadata.
  - Publishes prediction events to message bus (e.g., RabbitMQ/Redis Streams) and persists via Django API.
- **Django health bounded context** (`health` app):
  - Owns diseases, cows, predictions, disease records, model registry metadata.
  - Exposes REST endpoints for CRUD and querying predictions.
- **Data ingestion (FastAPI)**: Streams raw sensor payloads; enrich with `cow_id` mapping and forward to inference service asynchronously.

## Sensors for Mastitis and Wiring
- **Electrical Conductivity (EC)**: inline milk meters → LabVIEW Modbus/TCP → FastAPI ingestion → stored in `sensor_data`.
- **Somatic Cell Count (SCC)**: lab device integration via LabVIEW serial driver; batch upload via FastAPI.
- **pH & Milk Color**: optical/colorimetric sensors via LabVIEW DAQ; normalized to `[0,1]` features.
- **Udder Surface Temperature (IR)**: thermal camera; optional CNN pipeline; send summary stats (mean/max) per quarter.
- **Body Temperature**: rumen bolus or rectal probe sensors.
- **Activity/Motion & Rumination**: accelerometer collars; compute features (step count, lying bouts, rumination minutes).
- **Eating/Feed Intake**: load cells or RFID feed bins; join on `cow_id` using RFID tag mapping.

**LabVIEW → FastAPI bridge**: Each sensor channel publishes `{sensor_code, sensor_id, cow_external_id?, ts, value, unit}` to the ingestion HTTP endpoint. FastAPI enriches with `sensor_id`/`cow_id` via Django lookup before persisting.

## FastAPI Inference API (ai_service)
- `POST /api/v1/predictions` – body: `{cow_id, disease_code, model_name?, window_start, window_end, features:[...]}` → returns `{status, probability, prediction_id}` and emits event.
- `GET /api/v1/models` – list active models with metadata.
- `POST /api/v1/models/{model_id}/reload` – hot-reload artifact from `artifact_path`.
- `POST /api/v1/models/{model_id}/train` – kick off training job using labeled windows; store metrics and new version.
- `GET /api/v1/health` – readiness/liveness.

## Django REST (health app)
- `GET /api/health/cows/{id}/sensor-data?from=&to=&type=` – windowed series for dashboard.
- `GET /api/health/cows/{id}/predictions` – timeline of predictions.
- `POST /api/health/predictions` – persist prediction (used by ai_service callback).
- `POST /api/health/diseases` / `GET /api/health/diseases` – manage catalog.
- `POST /api/health/records` – create/update disease records (manual vet input or triggered by prediction).

## Training & Inference Workflow
1. **Ingestion**: LabVIEW sends sensor samples → FastAPI ingestion → `health_sensor_data` (plus existing `telemetry_sensor_readings`).
2. **Feature building**: Sliding window aggregation jobs (Celery/Prefect) compute per-cow feature vectors.
3. **Inference**: ai_service loads active `ml_models` artifacts, scores features, posts to `/api/health/predictions` (Django) and emits events.
4. **Record keeping**: Django creates/updates `disease_records` when thresholds crossed; alerts service can subscribe to prediction events.
5. **Retraining**: Scheduled job pulls labeled windows (`disease_records` + `sensor_data`), trains new model version, updates `ml_models` row and artifact URI.

## Model Recommendations
- **Tabular sensors**: RandomForest/XGBoost/Bayesian models for quick baselines; upgrade to Temporal CNN/LSTM for sequences.
- **Thermal imagery**: Lightweight CNN (MobileNet/ResNet18) with Grad-CAM for explainability.
- **Ensembling**: Stacking (meta-learner) to combine EC, SCC, temp, activity signals.
- **Versioning**: Store artifacts in object storage (S3/MinIO) with semantic version tags; track metrics in `ml_models.metrics`.

## Directory & File Additions
- `backend/services/user_management/health/` – Django bounded context with models, admin, migrations.
- `docs/architecture/disease_detection.md` – architecture, API specs, wiring instructions.
- ai_service (FastAPI) should host `/api/v1/predictions`, `/api/v1/models`, `/api/v1/health` within `backend/services/ai_service` (containerized separately).

## Node.js Dashboard Additions
- **Management screens**: CRUD for Diseases, Models, Sensors (types + instances), and Cow registry.
- **Analytics**: Time-series widgets per cow, current status badges (healthy/suspected), model accuracy charts, alert logs.
- **Extensibility**: Form-driven creation of diseases and models (no code changes); dropdowns pull from `diseases`, `ml_models`, and `sensors` APIs.

## Security & Contracts
- Keep disease data behind authenticated Django REST endpoints; ai_service uses service-token/JWT when posting predictions.
- No cross-database joins: ai_service reads only via REST or message bus; Django owns writes to disease tables.
