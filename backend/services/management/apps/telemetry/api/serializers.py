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
    activated_version = serializers.CharField()


class EdgeControllerTelemetryRequestSerializer(serializers.Serializer):
    edge_id = serializers.CharField()
    device_id = serializers.CharField()
    device_type = serializers.CharField()
    timestamp = serializers.CharField()
    metrics = serializers.DictField(child=serializers.FloatField())
    meta = serializers.DictField(required=False)


class EdgeControllerTelemetryResponseSerializer(serializers.Serializer):
    recorded = serializers.IntegerField()


class DataIngestionValidationRequestSerializer(serializers.Serializer):
    payload = serializers.DictField()


class DataIngestionValidationResponseSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    details = serializers.DictField(required=False)
