from django.urls import path
from .views import EventListView, EventAckView, EventResolveView

urlpatterns = [
    path("", EventListView.as_view()),
    path("<uuid:event_id>/ack/", EventAckView.as_view()),
    path("<uuid:event_id>/resolve/", EventResolveView.as_view()),
]
