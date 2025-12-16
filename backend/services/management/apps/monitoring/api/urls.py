from django.urls import path

from .views import LiveStatusListView

urlpatterns = [
    path("live-status/", LiveStatusListView.as_view(), name="live-status-list"),
]
