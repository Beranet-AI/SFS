# UC-03 Device & Edge Management

## Primary Actor
System / Operator

## Preconditions
- Edge node is deployed

## Main Flow
1. Edge node sends heartbeat
2. System registers or updates edge node
3. Edge reports discovered devices
4. Devices become eligible for telemetry ingestion

## Alternate Flow
- Edge goes offline → status marked accordingly

## Mapping
- edge_controller service
- Edge discovery sequence
