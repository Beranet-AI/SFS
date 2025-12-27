from django.http import JsonResponse
from apps.integrations.application.health_checks import HealthChecks


def health_check_view(request):
    checks = HealthChecks()
    return JsonResponse(
        {
            "ingestion": checks.ingestion(),
        }
    )
