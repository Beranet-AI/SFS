from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.incidents.application.services import IncidentService
from .serializers import IncidentCreateSerializer, IncidentSerializer


class IncidentListView(APIView):
    def get(self, request):
        service = IncidentService()
        incidents = service.list_incidents()
        data = [IncidentSerializer.from_entity(e) for e in incidents]
        return Response(data)

    def post(self, request):
        payload_serializer = IncidentCreateSerializer(data=request.data)
        payload_serializer.is_valid(raise_exception=True)
        service = IncidentService()
        incident = service.create(payload_serializer.validated_data)
        return Response(IncidentSerializer.from_entity(incident), status=status.HTTP_201_CREATED)


class IncidentAckView(APIView):
    def post(self, request, incident_id: str):
        service = IncidentService()
        incident = service.acknowledge(incident_id)
        return Response(IncidentSerializer.from_entity(incident))


class IncidentResolveView(APIView):
    def post(self, request, incident_id: str):
        service = IncidentService()
        incident = service.resolve(incident_id)
        return Response(IncidentSerializer.from_entity(incident))
