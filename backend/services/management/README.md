backend/services/management/
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
│
└── apps/
    ├── users/
    │   ├── domain/
    │   │   ├── entities.py        # User, Role (domain meaning)
    │   │   ├── value_objects.py   # Email, Phone, PasswordPolicy
    │   │   └── rules.py           # permission rules (domain-level)
    │   ├── application/
    │   │   ├── services.py        # UserService (create/assign roles)
    │   │   └── use_cases.py       # CreateUser, AssignRole
    │   ├── infrastructure/
    │   │   ├── models.py          # Django User/Role tables
    │   │   ├── repositories.py
    │   │   └── migrations/
    │   ├── api/
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   └── urls.py
    │   └── admin.py
    │
    ├── farms/
    │   ├── domain/
    │   │   ├── entities.py        # Farm, Barn, Greenhouse (as aggregates)
    │   │   ├── value_objects.py   # GeoPoint, Area, Capacity
    │   │   └── rules.py
    │   ├── application/
    │   │   ├── services.py
    │   │   └── use_cases.py
    │   ├── infrastructure/
    │   │   ├── models.py
    │   │   ├── repositories.py
    │   │   └── migrations/
    │   ├── api/
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   └── urls.py
    │   └── admin.py
    │
    ├── devices/
    │   ├── domain/
    │   │   ├── entities.py        # Device, SensorProfile, ActuatorProfile
    │   │   ├── value_objects.py   # DeviceId, DeviceKey, Endpoint
    │   │   ├── rules.py           # "pending cannot send commands" etc.
    │   │   └── events.py          # DeviceApproved, DeviceRevoked
    │   ├── application/
    │   │   ├── services.py        # DeviceService
    │   │   ├── discovery.py       # ApproveDiscovery, RejectDiscovery
    │   │   └── use_cases.py
    │   ├── infrastructure/
    │   │   ├── models.py          # Device + DiscoveryCandidate tables
    │   │   ├── repositories.py
    │   │   └── migrations/
    │   ├── api/
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   └── urls.py
    │   └── admin.py
    │
    ├── rules/
    │   ├── domain/
    │   │   ├── entities.py        # ThresholdRule, WindowRule
    │   │   ├── value_objects.py   # Metric, Comparator, WindowSize
    │   │   └── rules.py
    │   ├── application/
    │   │   ├── services.py
    │   │   └── use_cases.py
    │   ├── infrastructure/
    │   │   ├── models.py
    │   │   └── repositories.py
    │   └── api/
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    │
    ├── incidents/
    │   ├── domain/
    │   │   ├── entities.py        # Incident (status lifecycle)
    │   │   ├── value_objects.py   # Severity, Status
    │   │   └── rules.py           # resolve requires ack? (policy)
    │   ├── application/
    │   │   ├── services.py        # IncidentService
    │   │   └── use_cases.py       # Create, Ack, Resolve
    │   ├── infrastructure/
    │   │   ├── models.py
    │   │   └── repositories.py
    │   └── api/
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    │
    └── integrations/
        ├── application/
        │   └── health_checks.py
        └── infrastructure/
            ├── clients/
            │   ├── ingestion_client.py
            │   ├── monitoring_client.py
            │   ├── edge_client.py
            │   └── ai_client.py
            └── settings.py
