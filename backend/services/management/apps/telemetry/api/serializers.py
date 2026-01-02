# backend/services/management/apps/telemetry/api/serializers.py

from rest_framework import serializers


class ApproveTelemetrySchemaRequestSerializer(serializers.Serializer):
    """
    Input serializer for approving a telemetry schema.
    """

    approved = serializers.BooleanField(default=True)


class ApproveTelemetrySchemaResponseSerializer(serializers.Serializer):
    """
    Output serializer for approve schema response.
    """

    schema_id = serializers.UUIDField()
    status = serializers.CharField()
