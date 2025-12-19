from django.urls import path
from .views import LivestockView, LivestockHealthEvalView

urlpatterns = [
    path("", LivestockView.as_view()),
    path("<str:livestock_id>/evaluate-health/", LivestockHealthEvalView.as_view()),
]
