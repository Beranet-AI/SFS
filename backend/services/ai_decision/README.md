backend/services/ai_decision/
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
│   ├── inputs/
│   │   ├── __init__.py
│   │   └── telemetry_window.py
│   │
│   └── outputs/
│       ├── __init__.py
│       └── health_prediction.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── prediction_service.py
│       └── decision_pipeline.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── simple_health_model.py
│   │
│   └── clients/
│       ├── __init__.py
│       ├── management_client.py
│       └── telemetry_client.py
│
└── api/
    ├── __init__.py
    ├── schemas.py
    └── routes.py
