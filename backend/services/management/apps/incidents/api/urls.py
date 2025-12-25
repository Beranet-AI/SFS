from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_incidents),
    path("create/", views.create_incident),
]
