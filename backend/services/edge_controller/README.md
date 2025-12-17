backend/services/edge_controller/
└── app/
    ├── domain/
    │   ├── entities.py          # DiscoveredDevice, SensorReading
    │   ├── value_objects.py     # MacAddress, IpAddress, DeviceFingerprint
    │   └── rules.py             # "same fingerprint => same candidate"
    │
    ├── application/
    │   ├── discovery_service.py # scan_network(), build_report()
    │   ├── enrollment_service.py# send_report(), apply_config()
    │   └── telemetry_service.py # publish telemetry to ingestion
    │
    ├── infrastructure/
    │   ├── scanners/
    │   │   ├── mdns_scanner.py
    │   │   ├── modbus_scanner.py
    │   │   └── http_scanner.py
    │   ├── clients/
    │   │   └── management_client.py  # /devices/discovery/
    │   ├── mqtt_client.py
    │   └── local_store.py            # optional sqlite/redis (buffer)
    │
    ├── api/
    │   ├── routes.py             # local endpoints for ops
    │   └── schemas.py
    │
    └── main.py
