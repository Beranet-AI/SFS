apps/health/
├── __init__.py
├── apps.py
├── admin.py
│
├── domain/
│   ├── __init__.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   └── health_status.py
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   └── medical_record.py
│   │
│   ├── enums/
│   │   ├── __init__.py
│   │   └── diagnosis_type.py
│   │
│   └── repositories/
│       ├── __init__.py
│       └── medical_record_repo.py
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── record_diagnosis.py
│       └── update_health_status.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── medical_record_model.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── medical_record_repo_impl.py
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
