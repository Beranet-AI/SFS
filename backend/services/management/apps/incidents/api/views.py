from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import IncidentSerializer
from apps.incidents.application.services.incident_api_service import IncidentApiService


@api_view(["GET"])
def list_incidents(request):
    service = IncidentApiService()
    qs = service.list_incidents()
    return Response(IncidentSerializer(qs, many=True).data)


@api_view(["POST"])
def create_incident(request):
    ser = IncidentSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    service = IncidentApiService()
    obj = service.create_incident(validated_data=ser.validated_data)

    return Response(
        IncidentSerializer(obj).data,
        status=status.HTTP_201_CREATED,
    )
