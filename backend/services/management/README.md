backend/services/management/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
└── apps/
    ├── __init__.py
    │
    ├── users/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── admin.py
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   ├── entities/
    │   │   │   ├── __init__.py
    │   │   │   └── user.py
    │   │   ├── enums/
    │   │   │   ├── __init__.py
    │   │   │   └── role.py
    │   │   └── repositories/
    │   │       ├── __init__.py
    │   │       └── user_repo.py
    │   ├── application/
    │   │   ├── __init__.py
    │   │   └── use_cases/
    │   │       ├── __init__.py
    │   │       └── create_user.py
    │   ├── infrastructure/
    │   │   ├── __init__.py
    │   │   ├── models/
    │   │   │   ├── __init__.py
    │   │   │   └── user_model.py
    │   │   ├── repositories/
    │   │   │   ├── __init__.py
    │   │   │   └── user_repo_impl.py
    │   │   └── migrations/
    │   │       ├── __init__.py
    │   │       └── 0001_initial.py
    │   └── api/
    │       ├── __init__.py
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    │
    ├── farms/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── admin.py
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   ├── entities/
    │   │   │   ├── __init__.py
    │   │   │   └── farm.py
    │   │   └── repositories/
    │   │       ├── __init__.py
    │   │       └── farm_repo.py
    │   ├── application/
    │   │   ├── __init__.py
    │   │   └── use_cases/
    │   │       ├── __init__.py
    │   │       └── create_farm.py
    │   ├── infrastructure/
    │   │   ├── __init__.py
    │   │   ├── models/
    │   │   │   ├── __init__.py
    │   │   │   └── farm_model.py
    │   │   ├── repositories/
    │   │   │   ├── __init__.py
    │   │   │   └── farm_repo_impl.py
    │   │   └── migrations/
    │   │       ├── __init__.py
    │   │       └── 0001_initial.py
    │   └── api/
    │       ├── __init__.py
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    │
    ├── livestock/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── admin.py
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   ├── entities/
    │   │   │   ├── __init__.py
    │   │   │   └── livestock.py
    │   │   ├── value_objects/
    │   │   │   ├── __init__.py
    │   │   │   └── health_status.py
    │   │   ├── rules/
    │   │   │   ├── __init__.py
    │   │   │   └── health_rules.py
    │   │   └── repositories/
    │   │       ├── __init__.py
    │   │       └── livestock_repo.py
    │   ├── application/
    │   │   ├── __init__.py
    │   │   └── use_cases/
    │   │       ├── __init__.py
    │   │       └── update_health.py
    │   ├── infrastructure/
    │   │   ├── __init__.py
    │   │   ├── models/
    │   │   │   ├── __init__.py
    │   │   │   └── livestock_model.py
    │   │   ├── repositories/
    │   │   │   ├── __init__.py
    │   │   │   └── livestock_repo_impl.py
    │   │   └── migrations/
    │   │       ├── __init__.py
    │   │       └── 0001_initial.py
    │   └── api/
    │       ├── __init__.py
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    │
    ├── devices/
    │   └── ... (همان الگو: domain/application/infrastructure/api)
    ├── rules/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── admin.py
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   ├── rules_catalog.py
    │   │   └── policy_engine.py
    │   └── api/
    │       ├── __init__.py
    │       └── urls.py
    ├── telemetry/
    │   └── ... (ingest/query قرارداد + مدل ذخیره)
    ├── health/
    │   └── ... (medical_record entity + model + api)
    ├── incidents/
    │   └── ... (incident entity + model + api)
    └── integrations/
        ├── __init__.py
        ├── apps.py
        ├── application/
        │   ├── __init__.py
        │   └── health_checks.py
        └── infrastructure/
            ├── __init__.py
            ├── clients/
            │   ├── __init__.py
            │   ├── ingestion_client.py
            │   ├── monitoring_client.py
            │   ├── edge_client.py
            │   └── ai_client.py
            └── settings.py
