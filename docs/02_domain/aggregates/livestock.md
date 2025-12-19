# Aggregate: Livestock

## Root Entity
Livestock

## Identity
- LivestockId

## Attributes
- tag
- species (optional)
- current location (farm, barn, zone)

## Invariants
- A livestock must belong to exactly one farm location
- Livestock identity is immutable

## Associated Value Objects
- LivestockLocation

## Does NOT Contain
- Telemetry
- Health state
- Incidents

## Code Mapping
- management/apps/livestock/domain/
