from dataclasses import dataclass


@dataclass
class ApproveTelemetrySchemaInput:
    schema_id: str
    approved_by: str
