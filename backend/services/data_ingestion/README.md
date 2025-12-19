backend/services/data_ingestion/
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
│   └── telemetry_event.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── ingest_service.py
│       └── rule_dispatcher.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── management_client.py
│   │   ├── monitoring_client.py
│   │   └── rules_client.py
│   │
│   └── adapters/
│       ├── __init__.py
│       └── mqtt_adapter.py
│
└── api/
    ├── __init__.py
    ├── schemas.py
    └── routes.py
