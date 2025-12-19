from django.urls import path
from .views import FarmsView

urlpatterns = [
    path("", FarmsView.as_view()),
]
