livestock/
├── domain/
│   ├── entities/
│   │   └── livestock.py          # Aggregate Root
│   │
│   ├── value_objects/
│   │   ├── identity.py
│   │   ├── health_metrics.py
│   │   ├── nutrition_metrics.py
│   │   ├── milk_production.py
│   │   ├── reproduction.py
│   │   └── disease_record.py
│   │
│   ├── domain_services/
│   │   ├── livestock_health_analyzer.py
│   │   ├── livestock_risk_evaluator.py
│   │   └── livestock_ai_adapter.py
│   │
│   ├── domain_events/
│   │   ├── livestock_created.py
│   │   ├── health_anomaly_detected.py
│   │   ├── estrus_detected.py
│   │   ├── disease_diagnosed.py
│   │   └── treatment_completed.py
│   │
│   ├── repositories/
│   │   └── livestock_repository.py
│   │
│   ├── specifications/
│   │   ├── is_healthy.py
│   │   ├── requires_attention.py
│   │   ├── eligible_for_insemination.py
│   │   └── candidate_for_culling.py
│   │
│   └── exceptions/
│       └── livestock_domain_errors.py
│
├── application/
│   ├── livestock_service.py
│   │
│   └── use_cases/
│       ├── register_livestock/
│       │   ├── use_case.py
│       │   ├── input_dto.py
│       │   └── output_dto.py
│       │
│       ├── record_health_metrics/
│       │   ├── use_case.py
│       │   ├── input_dto.py
│       │   └── output_dto.py
│       │
│       ├── detect_health_anomaly/
│       │   ├── use_case.py
│       │   ├── input_dto.py
│       │   └── output_dto.py
│       │
│       ├── evaluate_reproduction_status/
│       │   ├── use_case.py
│       │   ├── input_dto.py
│       │   └── output_dto.py
│       │
│       ├── record_treatment/
│       │   ├── use_case.py
│       │   ├── input_dto.py
│       │   └── output_dto.py
│       │
│       └── generate_livestock_ai_insights/
│           ├── use_case.py
│           ├── input_dto.py
│           └── output_dto.py
│
├── api/
│   ├── base.py                  # BaseAPIView (DRF)
│   ├── urls.py                  # livestock routing
│   ├── views.py                 # DRF Views / APIViews
│   │
│   └── serializers/
│       ├── livestock_identity_serializer.py
│       ├── health_metrics_serializer.py
│       ├── nutrition_metrics_serializer.py
│       ├── milk_production_serializer.py
│       ├── reproduction_serializer.py
│       ├── disease_serializer.py
│       └── ai_insight_serializer.py
│
├── infrastructure/
│   ├── models.py                # Django ORM
│   ├── repositories.py          # LivestockRepositoryImpl
│   ├── mappers.py               # ORM ↔ Domain
│   ├── db.py
│   │
│   ├── admin/
│   │   ├── livestock_admin.py
│   │   └── health_record_admin.py
│   │
│   └── clients/
│       ├── telemetry_client.py
│       ├── ai_service_client.py
│       └── notification_client.py
│
└── apps.py
