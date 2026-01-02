from dataclasses import dataclass


@dataclass
class RegisterTelemetrySchemaOutput:
    device_id: str
    schema_id: str
    version: str
