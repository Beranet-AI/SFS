from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrService

from .models import LiveStatus, LiveStatusRule
from .serializers import LiveStatusRuleSerializer, LiveStatusSerializer


class LiveStatusRuleViewSet(viewsets.ModelViewSet):
    queryset = LiveStatusRule.objects.select_related("farm").all()
    serializer_class = LiveStatusRuleSerializer
    permission_classes = [IsAuthenticatedOrService]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


class LiveStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LiveStatus.objects.select_related(
        "farm",
        "barn",
        "zone",
        "sensor",
        "animal",
        "rule",
    ).all()
    serializer_class = LiveStatusSerializer
    permission_classes = [IsAuthenticatedOrService]

    def get_queryset(self):
        qs = super().get_queryset()
        farm_id = self.request.query_params.get("farm_id")
        state = self.request.query_params.get("state")
        severity = self.request.query_params.get("severity")
        zone_id = self.request.query_params.get("zone_id")
        sensor_id = self.request.query_params.get("sensor_id")
        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if state:
            qs = qs.filter(state=state)
        if severity:
            qs = qs.filter(severity=severity)
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs

    @action(detail=False, methods=["get"], url_path="active")
    def active_live_status(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(state="active")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ActiveLiveStatusView(APIView):
    permission_classes = [IsAuthenticatedOrService]

    def get(self, request, *args, **kwargs):
        qs = LiveStatus.objects.select_related(
            "farm",
            "barn",
            "zone",
            "sensor",
            "animal",
            "rule",
        ).filter(state="active")

        farm_id = request.query_params.get("farm_id")
        state = request.query_params.get("state")
        severity = request.query_params.get("severity")
        zone_id = request.query_params.get("zone_id")
        sensor_id = request.query_params.get("sensor_id")

        if farm_id:
            qs = qs.filter(farm_id=farm_id)
        if state:
            qs = qs.filter(state=state)
        if severity:
            qs = qs.filter(severity=severity)
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)

        serializer = LiveStatusSerializer(qs, many=True)
        return Response(serializer.data)
