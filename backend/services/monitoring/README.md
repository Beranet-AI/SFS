backend/services/monitoring/
├── __init__.py
├── main.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── lifespan.py
│
├── domain/
│   ├── __init__.py
│   └── livestatus.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── livestatus_service.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── cache/
│   │   ├── __init__.py
│   │   └── livestatus_store.py
│   │
│   └── clients/
│       ├── __init__.py
│       └── telemetry_client.py
│
└── api/
    ├── __init__.py
    ├── schemas.py
    └── routes.py
