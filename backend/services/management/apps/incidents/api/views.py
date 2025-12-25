from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.incidents.infrastructure.models.incident_model import IncidentModel
from .serializers import IncidentSerializer


@api_view(["GET"])
def list_incidents(request):
    qs = IncidentModel.objects.all().order_by("-ts")
    return Response(IncidentSerializer(qs, many=True).data)


@api_view(["POST"])
def create_incident(request):
    ser = IncidentSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    obj = ser.save()
    return Response(IncidentSerializer(obj).data, status=status.HTTP_201_CREATED)
