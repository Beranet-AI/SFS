# C4 – Level 2: Container Diagram

SFS is composed of multiple containers, each with a specific responsibility:

- WebApp (Next.js): User interface
- Management (Django): Source of Truth
- Data Ingestion (FastAPI): Telemetry intake
- Monitoring (FastAPI): Live read-only views
- AI Decision (FastAPI): Prediction and evaluation
- Edge Controller (FastAPI): Edge discovery and routing

Containers communicate exclusively via well-defined HTTP APIs.
No container shares a database with another.

See Mermaid / PlantUML diagrams:
- docs/03_architecture/c4/diagrams/C2-container.mmd
