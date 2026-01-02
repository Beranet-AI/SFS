# backend/services/management/apps/telemetry/application/services/schema_service.py


from ...infrastructure.models.schema_model import TelemetrySchemaModel


class SchemaService:
    """
    Query / coordination service for telemetry schemas
    """

    def get_active_schema(self, device_type: str) -> TelemetrySchemaModel:
        return TelemetrySchemaModel.objects.filter(
            device_type=device_type,
            is_active=True,
        ).first()

    def deactivate_active_schema(self, device_type: str):
        TelemetrySchemaModel.objects.filter(
            device_type=device_type,
            is_active=True,
        ).update(is_active=False)
