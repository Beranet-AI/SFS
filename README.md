## Architecture & Standards

For detailed architecture, conventions, and environment configuration:

- See `docs/architecture/ARCHITECTURE.md`
- See `docs/architecture/CONVENTIONS.md`
- See `docs/architecture/ENVIRONMENT.md`

# flowchart TD

%% ===================
%% SENSOR SIMULATION
%% ===================
LabVIEW["🟦 LabVIEW Sensor Simulator"]

%% ===================
%% EDGE LAYER
%% ===================
EdgeController["🟩 Edge Controller (Python / LabVIEW Bridge)"]

%% ===================
%% DATA INGESTION
%% ===================
DataIngestion["🟧 FastAPI - Data Ingestion Service"]

%% ===================
%% DJANGO (Core Backend)
%% ===================
Telemetry["🟪 Django Telemetry App"]
Livestock["🟫 Django Livestock App"]
Devices["🟨 Django Devices App"]
Users["🟦 Django Users App"]
Events["🟩 Django Events App (History Logs)"]

%% ===================
%% ALERTING MICROSERVICE
%% ===================
Alerting["🟥 FastAPI - Alerting Microservice"]

%% ===================
%% AI ENGINE
%% ===================
AIDecision["🟦 FastAPI - AI Decision Engine"]

%% ===================
%% FRONTEND
%% ===================
Frontend["🟩 Next.js Dashboard"]


%% -------- FLOWS --------

LabVIEW -->|Simulated Sensor Data| EdgeController

EdgeController -->|POST /ingest/data| DataIngestion

DataIngestion -->|POST /telemetry| Telemetry
DataIngestion -->|POST /livestock/update| Livestock

AIDecision -->|GET /telemetry/latest| Telemetry
AIDecision -->|GET /livestock/{id}| Livestock
AIDecision -->|GET /devices/sensors| Devices

AIDecision -->|POST /alerts/evaluate| Alerting

Alerting -->|POST /events/log| Events

Frontend -->|GET /telemetry| Telemetry
Frontend -->|GET /events| Events
Frontend -->|GET /livestock| Livestock
Frontend -->|GET /devices| Devices
Frontend -->|GET /users| Users

# sequenceDiagram

participant LabVIEW as LabVIEW Simulator
participant Edge as Edge Controller
participant Ingest as Data Ingestion
participant Telemetry as Django Telemetry App
participant Livestock as Django Livestock App
participant AI as AI Decision Engine
participant Alerting as Alerting Microservice
participant Events as Django Events App
participant FE as Dashboard (Next.js)

LabVIEW->>Edge: Sensor Data (temp, NH3, humidity, RFID…)
Edge->>Ingest: POST /ingest/data
Ingest->>Telemetry: POST /telemetry
Ingest->>Livestock: POST /livestock/update
Telemetry-->>AI: GET /telemetry/latest
Livestock-->>AI: GET /livestock/{id}

AI->>AI: Run ML Model / Detect anomaly
AI->>Alerting: POST /alerts/evaluate { risk_level }

Alerting->>Events: POST /events/log { alert, timestamp }
Events-->>FE: GET /events (history)
Telemetry-->>FE: GET /telemetry (live)

# Architecture Diagram

%% Hardware Layer
Sensors["Sensors / RFID / CameraAI"]
LabVIEW["LabVIEW Simulator"]

%% Edge Layer
Edge["🟩 Edge Controller (FastAPI)"]

%% Backend Layer
Ingestion["🟧 Data Ingestion Service (FastAPI)"]
AI["🟦 AI Decision Engine (FastAPI)"]
Alerting["🟥 Alerting Service (FastAPI)"]

Management["🔶 Django Management Service"]
Users["Users App"]
Telemetry["Telemetry App"]
Livestock["Livestock App"]
Devices["Devices App"]
Events["Events App (Logs)"]

DB["🗄 PostgreSQL Database"]

%% Frontend
Frontend["🟩 Web Dashboard (Next.js)"]

%% Flow
Sensors --> Edge
LabVIEW --> Edge
Edge --> Ingestion
Ingestion --> Management
Management --> DB
AI --> Management
AI --> Monitoring
Monitoring --> Incidents
Frontend --> Management
Frontend --> Incidents

# SmartFarm Architecture — IoT + Edge + Microservices + AI

This system collects sensor data from farm environments, processes it through an edge controller, ingests it into backend services, analyzes it using AI models, generates alerts, and visualizes the results in a modern dashboard.

Core Components
Edge Layer
LabVIEW simulator provides virtual sensor data
Edge Controller normalizes and forwards data securely

Backend Services

| Service                 | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| **data_ingestion**      | Entry point for sensor data                  |
| **management (Django)** | Users, Devices, Telemetry, Livestock, Incidents |
| **ai_decision**         | ML-based anomaly detection                   |
| **monitoring**          | Real-time live-status/alert stream           |

Frontend

Built with Next.js
Displays telemetry, alerts, events, and livestock status

# JSON Schema (Edge → Ingestion)

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EdgeSensorPayload",
  "type": "object",
  "properties": {
    "sensor_id": { "type": "string" },
    "sensor_type": { "type": "string", "enum": ["temperature", "humidity", "ammonia", "rfid", "camera_ai"] },
    "value": {},
    "unit": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "metadata": { "type": "object" }
  },
  "required": ["sensor_id", "sensor_type", "value", "timestamp"]
}
