from django.urls import path
from django.http import JsonResponse
from apps.integrations.application.health_checks import HealthChecks


def healthcheck(_request):
    """
    HTTP endpoint for integration health checks.
    """
    checks = HealthChecks()
    return JsonResponse(checks.check_all())


urlpatterns = [
    path("healthcheck/", healthcheck, name="integrations-healthcheck"),
]
