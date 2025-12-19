# C4 – Level 3: Component Diagram

Within the Management container, components are structured by bounded context:

- Livestock
- Telemetry
- Health
- Rules
- Incidents
- Farms

Each context follows Clean Architecture layering.
Components communicate through application services, not direct model access.

FastAPI containers have simpler component models focused on orchestration.

See Mermaid / PlantUML diagrams:
- docs/03_architecture/c4/diagrams/C3-component.mmd
