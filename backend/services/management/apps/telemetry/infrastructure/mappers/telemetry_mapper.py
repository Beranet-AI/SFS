# mappers/telemetry_mapper.py


from ...infrastructure.models.telemetry_model import TelemetryModel

class TelemetryMapper:
    def raw_to_domain(self, raw: dict) -> dict:
        return raw

    def domain_to_record(
        self,
        device_id: str,
        source: str,
        schema_version: str,
        telemetry_data: dict,
        received_at: int,
    ) -> TelemetryModel:
        metric = telemetry_data.get("metric")
        value = telemetry_data.get("value", telemetry_data)
        if metric is None and isinstance(telemetry_data.get("metrics"), dict):
            metric, value = next(
                iter(telemetry_data["metrics"].items()), ("raw", telemetry_data)
            )

        return TelemetryModel(
            device_id=device_id,
            device_type=telemetry_data.get("device_type", ""),
            metric=metric or "raw",
            value=value,
            source=source,
            schema_version=schema_version,
            payload=telemetry_data,
            recorded_at=received_at,
        )
