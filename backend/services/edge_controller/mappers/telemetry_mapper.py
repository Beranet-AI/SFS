from datetime import datetime

from ..application.use_cases.forward_telemetry.input_dto import (
    TelemetryInputDTO,
)
from ..application.use_cases.forward_telemetry.output_dto import (
    ForwardTelemetryOutputDTO,
)
from ..validators.telemetry_validator import validate_telemetry_payload


class InboundTelemetryMapper:
    @staticmethod
    def to_input(payload: dict) -> TelemetryInputDTO:
        """
        Map raw telemetry payload to TelemetryInput
        """
        validate_telemetry_payload(payload)

        return TelemetryInputDTO(
            edge_id=payload["edge_id"],
            device_id=payload["device_id"],
            device_type=payload["device_type"],
            timestamp=datetime.utcnow(),
            metrics=payload["metrics"],
            meta=payload.get("meta"),
        )


class OutboundTelemetryMapper:
    @staticmethod
    def to_response(dto: ForwardTelemetryOutputDTO) -> dict:
        return {"status": "FORWARDED" if dto.forwarded else "FAILED"}
