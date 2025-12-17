apps/health/
├── domain/
│   ├── entities.py
│   │   └── HealthRecord
│   │       - subject_type (animal / greenhouse)
│   │       - subject_id
│   │       - health_score
│   │       - status
│   │       - assessed_at
│   │
│   ├── value_objects.py
│   │   ├── HealthScore
│   │   ├── HealthStatus
│   │   └── AssessmentSource (AI / RULE / MANUAL)
│   │
│   └── rules.py
│       ├── is_critical()
│       └── requires_incident()
│
├── application/
│   ├── services.py
│   │   └── HealthService
│   │       - update_health()
│   │       - evaluate_health_status()
│   │
│   └── use_cases.py
│       ├── UpdateHealthFromAI
│       ├── UpdateHealthFromRule
│       └── GetHealthHistory
│
├── infrastructure/
│   ├── models.py
│   │   └── HealthRecordModel
│   │
│   ├── repositories.py
│   │   └── HealthRepository
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
