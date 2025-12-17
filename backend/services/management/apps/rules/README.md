apps/rules/
├── domain/
│   ├── entities.py
│   │   └── Rule
│   │       - id
│   │       - target_type (farm / greenhouse / device)
│   │       - target_id
│   │       - metric
│   │       - operator
│   │       - threshold_value
│   │       - window_sec
│   │       - severity
│   │       - enabled
│   │
│   ├── value_objects.py
│   │   ├── Metric
│   │   ├── Comparator (> < >= <=)
│   │   ├── Window
│   │   └── Severity
│   │
│   └── rules.py
│       ├── validate_metric_allowed()
│       ├── validate_window_logic()
│       └── can_trigger_incident()
│
├── application/
│   ├── services.py
│   │   └── RuleService
│   │       - create_rule()
│   │       - enable_rule()
│   │       - disable_rule()
│   │
│   └── use_cases.py
│       ├── CreateRule
│       ├── UpdateRule
│       └── ListActiveRules
│
├── infrastructure/
│   ├── models.py
│   │   └── RuleModel (Django ORM)
│   │
│   ├── repositories.py
│   │   └── RuleRepository
│   │       - save()
│   │       - get_active_for_target()
│   │
│   └── migrations/
│
├── api/
│   ├── serializers.py
│   │   └── RuleSerializer
│   │
│   ├── views.py
│   │   └── RuleViewSet
│   │
│   └── urls.py
│
├── admin.py
└── apps.py
