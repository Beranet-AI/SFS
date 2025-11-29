from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import Farm, Barn, Zone
from .serializers import FarmSerializer, BarnSerializer, ZoneSerializer


class IsActiveDefaultQuerysetMixin:
    """
    میکسین برای اینکه به‌صورت پیش‌فرض فقط رکوردهای is_active=True برگردند،
    مگر اینکه خلافش را خودت مشخص کنی.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class FarmViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]


class BarnViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Barn.objects.select_related("farm").all()
    serializer_class = BarnSerializer
    permission_classes = [permissions.IsAuthenticated]


class ZoneViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Zone.objects.select_related("barn", "barn__farm").all()
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]
