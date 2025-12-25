from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_devices),
    path("discoveries/", views.list_discoveries),
    path("discoveries/upsert/", views.upsert_discovery),
    path("discoveries/approve/", views.approve_discovery),
]
