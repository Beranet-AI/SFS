from rest_framework import serializers
from apps.events.domain.entities import Event


class EventSerializer(serializers.Serializer):
    id = serializers.CharField()
    severity = serializers.CharField()
    status = serializers.CharField()

    title = serializers.CharField()
    message = serializers.CharField()

    metric = serializers.CharField(allow_null=True)
    value = serializers.FloatField(allow_null=True)

    farm_id = serializers.CharField()
    barn_id = serializers.CharField(allow_null=True)
    zone_id = serializers.CharField(allow_null=True)
    device_id = serializers.CharField(allow_null=True)

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(allow_null=True)

    @staticmethod
    def from_entity(event: Event) -> dict:
        return EventSerializer(event).data
