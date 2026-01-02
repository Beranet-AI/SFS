from datetime import datetime

from .standardize_telemetry_input import StandardizeTelemetryInput
from .standardize_telemetry_output import StandardizeTelemetryOutput


class StandardizeTelemetryUseCase:
    def execute(
        self, input_dto: StandardizeTelemetryInput
    ) -> StandardizeTelemetryOutput:
        payload = input_dto.payload
        meta = payload.get("meta") or {}
        timestamp = payload.get("timestamp")
        if isinstance(timestamp, str):
            recorded_at = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        else:
            recorded_at = datetime.utcnow()

        standardized = []
        for metric, value in (payload.get("metrics") or {}).items():
            standardized.append(
                {
                    "device_id": payload.get("device_id"),
                    "device_type": payload.get("device_type"),
                    "metric": metric,
                    "value": value,
                    "unit": meta.get("unit"),
                    "source": input_dto.source,
                    "farm_id": meta.get("farm_id"),
                    "barn_id": meta.get("barn_id"),
                    "zone_id": meta.get("zone_id"),
                    "livestock_id": meta.get("livestock_id"),
                    "schema_version": meta.get("schema_version"),
                    "payload": payload,
                    "recorded_at": recorded_at,
                }
            )

        return StandardizeTelemetryOutput(standardized=standardized)
