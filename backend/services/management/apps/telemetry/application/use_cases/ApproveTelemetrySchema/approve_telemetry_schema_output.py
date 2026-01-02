from dataclasses import dataclass


@dataclass
class ApproveTelemetrySchemaOutput:
    schema_id: str
    status: str
    activated_version: str
