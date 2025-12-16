from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(...)  # بقیه resource ها

urlpatterns = [
    # 🔥 custom APIs FIRST
    path("api/v1/incidents/", include("apps.events.api.urls")),

    # router-based APIs LAST
    path("api/v1/", include(router.urls)),
]
