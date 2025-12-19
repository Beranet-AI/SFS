from django.urls import path
from .views import IncidentsView, IncidentAcknowledgeView, IncidentResolveView

urlpatterns = [
    path("", IncidentsView.as_view()),
    path("<str:incident_id>/ack/", IncidentAcknowledgeView.as_view()),
    path("<str:incident_id>/resolve/", IncidentResolveView.as_view()),
]
