# C4 – Level 4: Code Mapping

This level maps architectural elements directly to source code paths.

Examples:

- Livestock Aggregate
  → backend/services/management/apps/livestock/domain/

- Telemetry Ingestion Flow
  → edge_controller/api/
  → data_ingestion/api/
  → management/apps/telemetry/

- Incident Lifecycle
  → management/apps/incidents/domain/
  → management/apps/incidents/application/

This mapping is enforced via architecture guard tests.
