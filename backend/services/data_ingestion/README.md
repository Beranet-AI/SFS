backend/
└── services/
    └── edge_controller/
        ├── api/
        │   └── routes/
        │       ├── base.py
        │       ├── health.py
        │       ├── command.py                # single command endpoint
        │       └── __init__.py
        │
        ├── application/
        │   ├── edge_service.py               # Facade (single entry)
        │   │
        │   └── use_cases/
        │       ├── execute_command/
        │       │   ├── use_case.py            # Execute specific command
        │       │   ├── input_dto.py           # command_type, payload
        │       │   ├── output_dto.py          # execution result
        │       │   └── __init__.py
        │       │
        │       ├── listen_commands/
        │       │   ├── use_case.py            # MQTT / HTTP listener
        │       │   ├── input_dto.py
        │       │   ├── output_dto.py
        │       │   └── __init__.py
        │       │
        │       ├── dispatch_command/
        │       │   ├── use_case.py            # route by command.type
        │       │   ├── input_dto.py
        │       │   ├── output_dto.py
        │       │   └── __init__.py
        │       │
        │       ├── report_command_result/
        │       │   ├── use_case.py            # send result to management
        │       │   ├── input_dto.py
        │       │   ├── output_dto.py
        │       │   └── __init__.py
        │       │
        │       └── __init__.py
        │
        ├── domain/
        │   ├── entities/
        │   │   ├── edge_node.py
        │   │   ├── sensor_device.py           # approved sensor
        │   │   └── command_execution.py
        │   │
        │   └── events/
        │       ├── sensor_approved.py
        │       ├── sensor_removed.py
        │       └── command_executed.py
        │
        ├── infrastructure/
        │   ├── mqtt/
        │   │   ├── client.py                  # transport only
        │   │   └── topics.py
        │   │
        │   ├── scanners/                      # used by DISCOVER command
        │   │   ├── arp_scan.py
        │   │   ├── ping_probe.py
        │   │   ├── tcp_probe.py
        │   │   ├── classifier.py
        │   │   ├── payload_builder.py
        │   │   └── subnet_resolver.py
        │   │
        │   ├── telemetry/
        │   │   ├── environmental_listener.py  # env sensors
        │   │   ├── livestock_listener.py      # animal / plant sensors
        │   │   └── forwarder.py               # send to data_ingestion
        │   │
        │   └── registry/
        │       └── edge_registry.py            # runtime approved sensors
        │
        ├── mappers/
        │   ├── command_mapper.py               # contract → DTO
        │   └── telemetry_mapper.py
        │
        ├── core/
        │   ├── config.py
        │   ├── lifespan.py
        │   └── logging.py
        │
        ├── main.py
        ├── apps.py
        └── __init__.py
