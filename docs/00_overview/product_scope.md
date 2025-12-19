# Product Scope

## In Scope

SFS provides the following core capabilities:

1. Livestock Monitoring
   - Continuous telemetry ingestion (temperature, humidity, motion, etc.)
   - Live status visualization per livestock and per farm zone

2. Health Evaluation
   - Rule-based health assessment
   - AI-assisted health prediction (risk scoring)

3. Incident Management
   - Automatic incident creation from rules or AI predictions
   - Incident lifecycle management (open, acknowledged, resolved)

4. Device & Edge Management
   - Edge node discovery and heartbeat
   - Device metadata and association with livestock

5. Dashboard & Visualization
   - Web-based dashboard (Next.js)
   - Near real-time monitoring views
   - Historical and current state separation

## Out of Scope (Current Phase)

- Financial management
- Feed optimization
- Automated actuation (closing gates, medicine injection)
- Full mobile application (planned)

## Explicit Design Choice

SFS prioritizes **correctness, traceability, and evolvability**
over premature optimization or feature bloat.
