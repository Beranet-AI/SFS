# AI-Driven Mastitis Detection Blueprint

This document makes the mastitis detection stack implementation-ready while keeping the existing LabVIEW → FastAPI → Django → Node.js architecture intact. The same patterns generalize to other diseases and new sensor types.

## 1) Data Model Extensions (Django `health` app)
Field-level tables live in the `health` bounded context and own the disease domain data.

### `cows` (extends livestock registry)
- `animal_id` (FK → `livestock_animal`, unique)
- `lactation_stage` (`early|mid|late|dry`)
- `parity` (int)
- `breed` (char)
- `date_of_birth` (date)
- `days_in_milk` (int, nullable)
- `last_calving_date` (date, nullable)
- timestamps

### `diseases`
- `code` (unique), `name`, `description`
- `symptoms` (JSON array)
- `detection_methods` (JSON array)
- timestamps

### `ml_models`
- `name`, `version`, `framework` (sklearn/pytorch/tf/onnx)
- `disease_id` (FK → `diseases`)
- `artifact_path` (URI in object storage)
- `input_schema` (JSON feature list)
- `metrics` (JSON: AUC/F1/precision/recall/lead_time)
- `is_active` (bool)
- timestamps

### `sensor_data`
- `sensor_id` (FK → `devices_sensor`)
- `sensor_type_id` (FK → `devices_sensortype`)
- `cow_id` (FK → `cows`, nullable for ambient)
- `ts` (datetime, indexed)
- `value`, `unit`
- `aggregation` (`raw|minute|hourly|daily`)
- `sample_interval_seconds` (int, nullable)
- `quality` (`good|suspect|bad`)
- `raw_payload`
- `created_at`

### `predictions`
- `model_id` (FK → `ml_models`)
- `disease_id` (FK → `diseases`)
- `cow_id` (FK → `cows`)
- `status` (`healthy|suspected|at_risk`)
- `probability` (decimal)
- `lead_time_hours` (float, nullable)
- `predicted_at` (datetime, indexed)
- `features` (JSON)
- `feature_window_start`, `feature_window_end`

### `disease_records`
- `cow_id` (FK → `cows`)
- `disease_id` (FK → `diseases`)
- `status` (`suspected|confirmed|recovered`)
- `source_prediction_id` (FK → `predictions`, nullable)
- `diagnosed_at`, `resolved_at`
- `notes`

### New clinical and management logs
- `clinical_events`: `{cow_id, disease_id?, event_type (diagnosis|observation|treatment|lab), occurred_at, symptom, severity, source, notes}`
- `treatment_logs`: `{cow_id, disease_id?, clinical_event_id?, treatment_type, medication?, dose?, administered_by?, started_at, completed_at?, notes}`
- `lab_results`: `{cow_id, disease_id?, clinical_event_id?, parameter, value, unit?, result_at, reference_range?, notes}`
- `management_events`: `{cow_id?, event_type (pen_move|diet_change|milking_schedule|seasonal|other), description?, occurred_at, metadata}`

## 2) Input Data Requirements
- **Static cow metadata**: `cow_id`, parity, breed, DOB, last_calving_date, DIM (populate `days_in_milk`).
- **Time-series** (per sampling rules below): milk_yield, milk_conductivity, SCC, body_temperature, skin_temperature, rumination_time, activity_level, feed_intake, body_weight, ambient_temperature, milking_time.
- **Clinical events**: timestamped diagnosis/treatment/lab notes using `clinical_events`, `treatment_logs`, `lab_results`.
- **Management events**: pen moves, diet changes, milking schedule updates via `management_events`.

## 3) Sensor Integration
- **LabVIEW drivers**: extend channel map to include EC/SCC analyzers, rumination collars, load-cell scales, IR thermometers/cameras, feed-intake bins, and neck-collar accelerometers.
- **Payload format**: `{sensor_code, sensor_id, cow_external_id?, ts, value, unit, aggregation?, sample_interval_seconds?}`.
- **FastAPI ingestion**: enrich payloads with `sensor_id`/`cow_id` via Django lookup, persist to `sensor_data`, and forward windows to AI inference service async.
- **Manual entry**: mobile/web form posts to Django `clinical_events` for lab/clinical notes.

## 4) Sampling Frequency (standardize in ingestion jobs)
- Milk yield/EC/SCC: **per milking** (3x daily typical).
- Activity/rumination: **raw 1-minute** → aggregate hourly + daily.
- Body/skin temp: **daily** or per milking; IR camera aggregates per session.
- Weight/feed intake: **daily** (post-milking exit lane scale, feed bin totals).
- Clinical/management events: **real-time** with precise timestamps.

## 5) Labeling Strategy
- Ground truth: clinical diagnosis events (`clinical_events.event_type=diagnosis`).
- Positive windows: 24–72h before diagnosis.
- Negative windows: ≥7 days away from any diagnosis.
- Handle imbalance: class weights, oversampling, focal loss; support active learning by flagging low-confidence predictions for manual labeling.

## 6) Feature Engineering
- Moving averages/deltas: 24h/48h/7d for EC, yield, rumination, temperature, weight.
- Z-score per cow to normalize individual baselines.
- Cross-features: milk/weight ratio, rumination drops vs. baseline, activity variance.
- Missing data: forward-fill within short gaps; longer gaps get explicit missing indicators.

## 7) Model Pipeline
- **Models**: start with RandomForest/XGBoost baselines; add LSTM for sequential signals; optional CNN for IR frames.
- **Containers**: package training + inference as Docker images; load artifacts from object storage (S3/MinIO) based on `ml_models.artifact_path`.
- **Training**: cron/Prefect/Celery job pulls labeled windows (sensor_data + disease_records), trains, logs metrics, writes new model version row, uploads artifact.
- **Inference**: FastAPI ai_service loads active model per disease, scores recent window, returns `{status, probability, lead_time_hours}` and posts to Django.

## 8) FastAPI AI Service (new `ai_service` or embedded in data ingestion)
- `POST /api/v1/predict/mastitis` → body: `{cow_id, window_start, window_end, features?:{...}}` OR server-side window fetch; returns `{prediction_id, status, probability, lead_time_hours, feature_window_start, feature_window_end}`.
- `GET /api/v1/predictions?cow_id=&disease_code=&limit=` → list predictions.
- `POST /api/v1/train/model` → `{disease_code, model_name, version?, training_window_days?, labels_source?}` triggers training job.
- `GET /api/v1/features/importance?model_id=` → returns top features (Gain/SHAP if available).
- `GET /api/v1/models` / `POST /api/v1/models/{id}/reload` to manage active artifacts.

## 9) Django REST (health app)
- `GET /api/health/cows/{id}/sensor-data?from=&to=&type=&agg=`
- `GET /api/health/cows/{id}/predictions`
- `POST /api/health/predictions` (callback from ai_service)
- `POST /api/health/clinical-events` / `treatment-logs` / `lab-results` / `management-events`
- CRUD for diseases, models, cows

## 10) Node.js Dashboard Additions
- Disease board: per-cow status badges (healthy/suspected/at_risk) + probability sparkline.
- Time-series charts: EC, SCC, yield, rumination, temp, weight with thresholds and sampling aggregation switcher.
- Management UI: add/remove diseases, sensors, models; assign sensors to cows/locations.
- Clinical & treatment timeline: forms for events/labs/treatments; link predictions to records.
- Model ops: upload new model artifact/metadata, set active version, view metrics and feature importance.
- Analytics: recall/precision/lead-time charts; false-alarm log.

## 11) Deployment & Evaluation
- Pilot 50–100 cows; collect ≥3 months of data; manual labels via `clinical_events`.
- Sync timestamps across LabVIEW/FastAPI/Django; enforce UTC.
- Metrics to track: recall (early detection), precision, lead time, AUC/F1; alert volume vs. resolved cases.
- Rollout: start with tree-based model; iterate with LSTM when sequence depth is sufficient; gate releases via canary in ai_service.

## 12) Directory/Service Touch Points
- Django: `backend/services/user_management/health/` models/admin/migrations already own schema.
- FastAPI: add ai_service under `backend/services/ai_service/` (Dockerized) or extend data_ingestion with the endpoints above.
- LabVIEW: extend channel map and payload to include new sensors; send to FastAPI ingestion.
- Node.js: add dashboard modules described above; call Django/ai_service APIs, no server restarts for new diseases/models.

Security: ai_service authenticates to Django via service token/JWT; no cross-database joins—only API/event calls. All new disease/sensor/model records are data-driven and require no code changes.
