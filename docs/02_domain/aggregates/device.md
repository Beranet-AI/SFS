# Aggregate: Device

## Root Entity
Device

## Identity
- DeviceId

## Attributes
- device type
- edge association
- livestock association (optional)

## Invariants
- A device belongs to at most one livestock at a time
- Device type is immutable after registration

## Code Mapping
- management/apps/devices/
- edge_controller discovery
