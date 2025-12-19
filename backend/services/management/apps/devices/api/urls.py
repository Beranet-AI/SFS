from django.urls import path
from .views import DevicesView, DeviceAssignView

urlpatterns = [
    path("", DevicesView.as_view()),
    path("<str:device_id>/assign/", DeviceAssignView.as_view()),
]
