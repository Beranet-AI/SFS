apps/telemetry/
├── domain/
│   ├── entities.py
│   │   └── TelemetrySnapshot
│   │       - device_id
│   │       - metric
│   │       - value
│   │       - recorded_at
│   │
│   ├── value_objects.py
│   │   ├── Metric
│   │   ├── Unit
│   │   └── Timestamp
│   │
│   └── rules.py
│       ├── is_fresh()
│       └── can_update_snapshot()
│
├── application/
│   ├── services.py
│   │   └── TelemetryService
│   │       - update_snapshot()
│   │       - get_latest_for_device()
│   │
│   └── use_cases.py
│       ├── UpdateTelemetrySnapshot
│       └── GetLatestTelemetry
│
├── infrastructure/
│   ├── models.py
│   │   └── TelemetrySnapshotModel
│   │
│   ├── repositories.py
│   │   └── TelemetryRepository
│   │
│   └── migrations/
│
├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── admin.py
└── apps.py
