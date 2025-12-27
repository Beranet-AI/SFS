backend/
└── shared/
    ├── __init__.py
    │
    ├── ids/
    │   ├── __init__.py
    │   ├── base_id.py
    │   ├── livestock_id.py
    │   ├── device_id.py
    │   ├── farm_id.py
    │   └── incident_id.py
    │
    ├── enums/
    │   ├── __init__.py
    │   ├── health_state.py
    │   ├── device_type.py
    │   ├── incident_severity.py
    │   └── incident_status.py
    │
    ├── value_objects/
    │   ├── __init__.py
    │   └── livestock_location.py
    │
    └── dto/
        ├── __init__.py
        ├── livestock_dto.py
        ├── health_status_dto.py
        ├── incident_dto.py
        └── livestatus_dto.py



# Shared Kernel – SFS

This module contains immutable domain primitives shared across backend services.

## Allowed
- Value Objects
- DTOs
- IDs
- Enums

## Forbidden
- ORM models
- Repositories
- Services
- IO / Network / DB access

Any violation of these rules is considered an architectural error.
