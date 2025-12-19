apps/devices/
├── __init__.py
├── apps.py
├── admin.py
│
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── device.py
│   │
│   ├── enums/
│   │   ├── __init__.py
│   │   └── device_status.py
│   │
│   ├── value_objects/
│   │   ├── __init__.py
│   │   └── device_assignment.py
│   │
│   └── repositories/
│       ├── __init__.py
│       └── device_repo.py
│
├── application/
│   ├── __init__.py
│   └── use_cases/
│       ├── __init__.py
│       ├── register_device.py
│       ├── assign_device.py
│       └── change_device_status.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── device_model.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── device_repo_impl.py
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
