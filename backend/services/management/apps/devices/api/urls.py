from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_devices),
    path("discoveries/", views.list_discoveries),
    path("discoveries/upsert/", views.upsert_discovery),
    path("discoveries/approve/", views.approve_discovery),
    path(
        "environmental-sensors/register/",
        views.register_environmental_sensor,
    ),
    path("control-devices/register/", views.register_control_device),
]
