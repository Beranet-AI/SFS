from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import AlertRule, Alert
from .serializers import AlertRuleSerializer, AlertSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.select_related("farm").all()
    serializer_class = AlertRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related(
        "farm",
        "barn",
        "zone",
        "sensor",
        "animal",
        "rule",
    ).all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        farm_id = self.request.query_params.get("farm_id")
        status = self.request.query_params.get("status")
        severity = self.request.query_params.get("severity")
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if status:
            qs = qs.filter(status=status)
        if severity:
            qs = qs.filter(severity=severity)
        return qs
