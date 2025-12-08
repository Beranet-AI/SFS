from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import AlertLog, AlertRule
from alerts.serializers import AlertLogSerializer, AlertRuleSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.select_related("sensor", "sensor__sensor_type")
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        sensor_id = self.request.query_params.get("sensor_id")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs


class AlertLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertLog.objects.select_related(
        "sensor",
        "sensor__sensor_type",
        "alert_rule",
    )
    serializer_class = AlertLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        sensor_id = self.request.query_params.get("sensor_id")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs


class ActiveAlertsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        sensor_id = request.query_params.get("sensor_id")
        limit = int(request.query_params.get("limit", 20))

        qs = AlertLog.objects.select_related("sensor", "alert_rule")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        latest_alerts = qs.order_by("-triggered_at")[:limit]

        serializer = AlertLogSerializer(latest_alerts, many=True)
        return Response({"alerts": serializer.data})
