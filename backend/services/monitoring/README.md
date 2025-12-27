backend/services/monitoring/
├── main.py
├── api/
│   ├── routes.py
│   └── sse.py
│
├── core/
│   ├── config.py
│   └── lifespan.py
│
├── domain/
│   ├── device_health_state.py
│   ├── enums.py
│   ├── value_objects.py
│   └── events/
│       ├── livestatus_event.py
│       └── device_offline_event.py
│
├── application/
│   ├── services/
│   │   ├── device_health_service.py
│   │   ├── livestatus_service.py
│   │   └── rule_evaluator_service.py
│   │
│   ├── streams/
│   │   └── livestatus_event_stream.py
│   │
│   └── dispatchers/
│       ├── incident_dispatcher.py
│       └── command_dispatcher.py
│
├── infrastructure/
│   ├── repositories/
│   │   └── heartbeat_repository.py
│   │
│   └── clients/
│       ├── management_client.py
│       └── command_client.py
│
└── dto/
    ├── livestatus_dto.py
    └── health_status_dto.py
