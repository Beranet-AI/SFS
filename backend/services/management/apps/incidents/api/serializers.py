from rest_framework import serializers
from apps.incidents.models import IncidentModel


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentModel
        fields = "__all__"
