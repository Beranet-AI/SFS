# UC-01 Livestock Monitoring

## Primary Actor
Farm Operator

## Preconditions
- Livestock is registered
- Devices are associated

## Main Flow
1. Device emits telemetry
2. Telemetry is ingested
3. Live status is updated
4. Operator views live dashboard

## Alternate Flows
- Telemetry delayed → previous snapshot shown
- Monitoring service unavailable → system continues ingesting telemetry

## Postconditions
- No persistent state is modified by monitoring

## Mapping
- monitoring service
- Sequence: Live Monitoring
- Test: monitoring read-only tests
