farm/
├── domain/
│   ├── entities/
│   │   ├── farm.py            # Aggregate Root
│   │   ├── barn.py
│   │   └── zone.py
│   │
│   ├── value_objects/
│   │   ├── location.py
│   │   ├── environmental_metrics.py
│   │   ├── economic_metrics.py
│   │   └── capacity.py
│   │
│   ├── domain_services/
│   │   ├── environment_analyzer.py
│   │   └── farm_ai_adapter.py
│   │
│   ├── domain_events/
│   │   ├── farm_created.py
│   │   ├── barn_added.py
│   │   ├── zone_added.py
│   │   ├── zone_environment_threshold_exceeded.py
│   │   └── farm_cost_anomaly_detected.py
│   │
│   ├── repositories/
│   │   └── farm_repository.py
│   │
│   ├── specifications/
│   │   ├── optimal_zone_environment.py
│   │   ├── barn_heat_stress_risk.py
│   │   └── farm_requires_intervention.py
│   │
│   └── exceptions/
│       └── farm_domain_errors.py
│
├── application/
│   ├── farm_service.py
│   │
│   └── use_cases/
│       ├── register_farm/
│       ├── register_barn/
│       ├── register_zone/
│       ├── record_zone_environment_metrics/
│       ├── record_farm_economic_metrics/
│       ├── detect_zone_environment_risk/
│       └── generate_farm_ai_insights/
│
├── api/
│   ├── base.py
│   ├── urls.py
│   ├── views.py
│   └── serializers/
│       ├── farm_serializer.py
│       ├── barn_serializer.py
│       ├── zone_serializer.py
│       ├── environment_metrics_serializer.py
│       ├── economic_metrics_serializer.py
│       └── ai_insight_serializer.py
│
├── infrastructure/
│   ├── models.py
│   ├── repositories.py
│   ├── mappers.py
│   ├── db.py
│   ├── admin/
│   │   ├── farm_admin.py
│   │   ├── barn_admin.py
│   │   └── zone_admin.py
│   └── clients/
│       ├── sensor_gateway_client.py
│       └── ai_service_client.py
│
└── apps.py
