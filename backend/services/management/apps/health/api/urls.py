from django.urls import path
from .views import MedicalRecordsView

urlpatterns = [
    path("<str:livestock_id>/records/", MedicalRecordsView.as_view()),
]
