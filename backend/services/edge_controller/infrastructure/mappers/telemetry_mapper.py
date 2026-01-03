from datetime import datetime

from ...application.use_cases.forward_telemetry.input_dto import (
    TelemetryInputDTO,
)
from ...application.use_cases.forward_telemetry.output_dto import (
    ForwardTelemetryOutputDTO,
)

class InboundTelemetryMapper:
    @staticmethod
    def to_input(payload: dict) -> TelemetryInputDTO:
        """
        Map raw telemetry payload to TelemetryInput
        """
        timestamp = payload.get("timestamp")
        if isinstance(timestamp, str):
            parsed_timestamp = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        else:
            parsed_timestamp = datetime.utcnow()

        return TelemetryInputDTO(
            edge_id=payload["edge_id"],
            device_id=payload["device_id"],
            device_type=payload["device_type"],
            timestamp=parsed_timestamp,
            metrics=payload["metrics"],
            meta=payload.get("meta"),
        )


class OutboundTelemetryMapper:
    @staticmethod
    def to_response(dto: ForwardTelemetryOutputDTO) -> dict:
        return {"status": "FORWARDED" if dto.forwarded else "FAILED"}
