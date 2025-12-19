backend/services/edge_controller/
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
│   ├── edge_node.py
│   └── discovery_event.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── discovery_service.py
│       └── forward_service.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── registry/
│   │   ├── __init__.py
│   │   └── edge_registry.py
│   │
│   └── clients/
│       ├── __init__.py
│       └── ingestion_client.py
│
└── api/
    ├── __init__.py
    ├── schemas.py
    └── routes.py
