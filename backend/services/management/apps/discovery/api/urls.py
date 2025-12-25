from django.urls import path
from apps.discovery.api import views

urlpatterns = [
    path("discovery/devices", views.upsert_discovery),
    path("discovery/pending", views.list_pending),
    path("discovery/<str:external_id>/approve", views.approve),
]
