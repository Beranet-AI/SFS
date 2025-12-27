from django.urls import path
from .views import FarmsView, FarmDetailView

urlpatterns = [
    path("", FarmsView.as_view()),
    path("<int:farm_id>/", FarmDetailView.as_view()),
]
