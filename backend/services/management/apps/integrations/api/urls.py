from django.urls import path
from django.http import JsonResponse
from apps.integrations.application.health_checks import HealthChecks

def healthcheck(_request):
    hc = HealthChecks()
    return JsonResponse(hc.check_all())

urlpatterns = [
    path("healthcheck/", healthcheck),
]
