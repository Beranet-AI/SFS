from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAuthenticatedOrService
from .models import Alert, AlertRule
from .serializers import AlertRuleSerializer, AlertSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.select_related("farm").all()
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticatedOrService]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


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
    permission_classes = [IsAuthenticatedOrService]

    def get_queryset(self):
        qs = super().get_queryset()
        farm_id = self.request.query_params.get("farm_id")
        status = self.request.query_params.get("status")
        severity = self.request.query_params.get("severity")
        zone_id = self.request.query_params.get("zone_id")
        sensor_id = self.request.query_params.get("sensor_id")
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if status:
            qs = qs.filter(status=status)
        if severity:
            qs = qs.filter(severity=severity)
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs

    @action(detail=False, methods=["get"], url_path="active")
    def active_alerts(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(status="open")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
