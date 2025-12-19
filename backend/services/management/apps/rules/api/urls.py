from django.urls import path
from django.http import JsonResponse
from apps.rules.domain.policy_engine import PolicyEngine

def rules_list(_request):
    engine = PolicyEngine()
    return JsonResponse(engine.list_rules())

urlpatterns = [
    path("", rules_list),
]
