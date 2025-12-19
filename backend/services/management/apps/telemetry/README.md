apps/telemetry/
├── __init__.py
├── apps.py
├── admin.py
│
├── domain/
│   ├── __init__.py
│   ├── records/
│   │   ├── __init__.py
│   │   └── telemetry_record.py
│   │
│   └── repositories/
│       ├── __init__.py
│       └── telemetry_repo.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── ingest_telemetry.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── telemetry_model.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── telemetry_repo_impl.py
│   │
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
└── api/
    ├── __init__.py
    ├── serializers.py
    ├── views.py
    └── urls.py
