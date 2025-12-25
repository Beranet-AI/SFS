from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_commands),
    path("send/", views.send_command),
]
