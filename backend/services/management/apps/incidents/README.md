apps/incidents/
├── domain/
│   ├── entities.py
│   │   └── Incident
│   │       - id
│   │       - device_id
│   │       - metric
│   │       - observed_value
│   │       - threshold
│   │       - severity
│   │       - status
│   │       - opened_at
│   │       - acked_at
│   │       - resolved_at
│   │
│   ├── value_objects.py
│   │   ├── Severity
│   │   ├── IncidentStatus
│   │   └── ResolutionNote
│   │
│   └── rules.py
│       ├── can_ack()
│       ├── can_resolve()
│       └── is_terminal_state()
│
├── application/
│   ├── services.py
│   │   └── IncidentService
│   │       - create_incident()
│   │       - ack_incident()
│   │       - resolve_incident()
│   │
│   └── use_cases.py
│       ├── CreateIncident
│       ├── AckIncident
│       └── ResolveIncident
│
├── infrastructure/
│   ├── models.py
│   │   └── IncidentModel
│   │
│   ├── repositories.py
│   │   └── IncidentRepository
│   │       - save()
│   │       - get_open()
│   │       - get_by_device()
│   │
│   └── migrations/
│
├── api/
│   ├── serializers.py
│   │   ├── IncidentSerializer
│   │   ├── AckSerializer
│   │   └── ResolveSerializer
│   │
│   ├── views.py
│   │   └── IncidentViewSet
│   │
│   └── urls.py
│
├── admin.py
└── apps.py
