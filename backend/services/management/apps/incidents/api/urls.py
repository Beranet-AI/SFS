
from django.urls import path

from .views import IncidentAckView, IncidentListView, IncidentResolveView

urlpatterns = [
    path("", IncidentListView.as_view(), name="incident-list"),
    path("<uuid:incident_id>/ack/", IncidentAckView.as_view(), name="incident-ack"),
    path("<uuid:incident_id>/resolve/", IncidentResolveView.as_view(), name="incident-resolve"),
]
