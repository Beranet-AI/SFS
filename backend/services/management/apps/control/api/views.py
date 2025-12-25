from rest_framework.viewsets import ModelViewSet
from apps.control.models import CommandModel
from apps.control.api.serializers import CommandSerializer

class CommandViewSet(ModelViewSet):
    queryset = CommandModel.objects.all().order_by("-created_at")
    serializer_class = CommandSerializer
