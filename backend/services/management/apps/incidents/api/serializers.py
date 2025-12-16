from rest_framework import serializers

from apps.incidents.domain.entities import Incident
from apps.incidents.domain.enums import IncidentStatus


class IncidentSerializer(serializers.Serializer):
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
    def from_entity(incident: Incident) -> dict:
        return IncidentSerializer(incident).data


class IncidentCreateSerializer(serializers.Serializer):
    severity = serializers.CharField()
    status = serializers.CharField(default=IncidentStatus.RAISED.value)
    title = serializers.CharField()
    message = serializers.CharField()
    metric = serializers.CharField(allow_null=True, required=False)
    value = serializers.FloatField(allow_null=True, required=False)
    farm_id = serializers.CharField()
    barn_id = serializers.CharField(allow_null=True, required=False)
    zone_id = serializers.CharField(allow_null=True, required=False)
    device_id = serializers.CharField(allow_null=True, required=False)
