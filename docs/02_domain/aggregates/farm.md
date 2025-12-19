# Aggregate: Farm

## Root Entity
Farm

## Identity
- FarmId

## Attributes
- name
- geographic metadata
- barns and zones

## Invariants
- A barn belongs to exactly one farm
- A zone belongs to exactly one barn

## Associated Value Objects
- LivestockLocation (composition)

## Code Mapping
- management/apps/farms/
