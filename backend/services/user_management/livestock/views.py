from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import Animal, RfidTag
from .serializers import AnimalSerializer, RfidTagSerializer


class RfidTagViewSet(viewsets.ModelViewSet):
    queryset = RfidTag.objects.select_related("farm").all()
    serializer_class = RfidTagSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.select_related(
        "farm",
        "barn",
        "current_zone",
        "rfid_tag",
    ).all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]
