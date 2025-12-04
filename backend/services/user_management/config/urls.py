from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("sensor-readings/", views.SensorReadingView.as_view(), name="sensor-reading"),
    path("sensors/<int:pk>/", views.SensorDetailView.as_view(), name="sensor-detail"),
]
