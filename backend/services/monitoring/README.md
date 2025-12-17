backend/services/monitoring/
└── app/
    ├── application/
    │   ├── live_status_query.py     # latest telemetry per device/metric
    │   └── health_query.py
    │
    ├── infrastructure/
    │   ├── tsdb_reader.py
    │   ├── cache_reader.py          # optional
    │   └── clients/
    │       └── management_client.py # device metadata
    │
    ├── api/
    │   ├── routes.py                # /live-status, /devices/{id}/latest
    │   └── schemas.py
    │
    └── main.py
