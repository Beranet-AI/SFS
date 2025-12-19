from rest_framework import serializers

class IncidentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    livestock_id = serializers.CharField()
    severity = serializers.CharField()
    status = serializers.CharField()
    source = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    acknowledged_at = serializers.DateTimeField(allow_null=True)
    resolved_at = serializers.DateTimeField(allow_null=True)
