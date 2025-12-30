backend/
└── services/
    └── edge_controller/
        ├── api/
        │   └── routes/
        │       ├── base.py
        │       ├── health.py
        │       ├── command.py
        │       └── __init__.py
        │
        ├── application/
        │   ├── edge_service.py
        │   │
        │   ├── common/                         # envelopes (shared inside service)
        │   │   ├── command_base.py
        │   │   ├── command_result_base.py
        │   │   ├── error.py
        │   │   └── __init__.py
        │   │
        │   └── services/
        │       └── use_cases/
        │           ├── listen_commands/
        │           │   ├── use_case.py
        │           │   ├── input_dto.py
        │           │   └── output_dto.py
        │           │
        │           ├── dispatch_command/
        │           │   ├── use_case.py
        │           │   ├── input_dto.py
        │           │   └── output_dto.py
        │           │
        │           ├── execute_command/
        │           │   ├── use_case.py
        │           │   ├── input_dto.py
        │           │   └── output_dto.py
        │           │
        │           └── report_command_result/
        │               ├── use_case.py
        │               ├── input_dto.py
        │               └── output_dto.py
        │
        ├── mappers/
        │   ├── command_mapper.py               # JSON → Command DTO
        │   ├── result_mapper.py                # Result DTO → JSON
        │   └── __init__.py
        │
        ├── infrastructure/
        │   ├── mqtt/                           # 🔵 OT – device side
        │   │   ├── device_client.py            # send commands to devices
        │   │   ├── device_topics.py            # device topic constants
        │   │   └── __init__.py
        │   │
        │   ├── client/                         # 🟢 IT – software side
        │   │   ├── commands_client.py          # send results to command source
        │   │   ├── data_ingestion_client.py    # send telemetry
        │   │   ├── monitoring_client.py        # optional
        │   │   └── __init__.py
        │   │
        │   └── registry/
        │       └── edge_registry.py            # approved / active devices
        │
        ├── core/
        │   ├── config.py
        │   ├── logging.py
        │   └── lifespan.py
        │
        ├── main.py
        └── __init__.py
