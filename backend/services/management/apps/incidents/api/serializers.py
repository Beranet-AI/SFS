from rest_framework import serializers
from apps.incidents.infrastructure.models.incident_model import IncidentModel


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentModel
        fields = "__all__"
