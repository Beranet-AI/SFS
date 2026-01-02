# backend/services/management/apps/telemetry/application/services/schema_service.py


from ...api.schemas.telemetry_schema import TelemetrySchema


class SchemaService:
    """
    Query / coordination service for telemetry schemas
    """

    def get_active_schema(self, device_type: str) -> TelemetrySchema:
        return TelemetrySchema.objects.filter(
            device_type=device_type,
            is_active=True,
        ).first()

    def deactivate_active_schema(self, device_type: str):
        TelemetrySchema.objects.filter(
            device_type=device_type,
            is_active=True,
        ).update(is_active=False)
