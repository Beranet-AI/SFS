backend/services/data_ingestion/
└── app/
    ├── domain/
    │   ├── entities.py          # TelemetryPoint
    │   ├── value_objects.py     # MetricKind, Unit, Timestamp
    │   ├── rules.py             # validation rules
    │   └── policies.py          # threshold evaluation policies
    │
    ├── application/
    │   ├── ingest_use_case.py   # receive -> validate -> store
    │   ├── evaluate_rules.py    # check threshold/window rules
    │   └── emit_incident.py     # call management incidents API
    │
    ├── infrastructure/
    │   ├── tsdb/
    │   │   ├── writer.py        # write telemetry
    │   │   └── reader.py
    │   ├── cache/
    │   │   └── redis_cache.py   # optional live aggregation
    │   ├── clients/
    │   │   ├── management_client.py  # rules + incident create
    │   │   └── edge_client.py
    │   └── settings.py
    │
    ├── api/
    │   ├── routes.py            # /telemetry/ingest
    │   └── schemas.py
    │
    └── main.py
