from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.serializers.get_command_serializer import GetCommandSerializer
from apps.commands.application.use_cases.get_command.use_case import (
    GetCommandUseCase,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)


class GetCommandView(BaseController):
    """
    GET /commands/{id}/
    """

    serializer_class = GetCommandSerializer

    def get(self, request, command_id):
        serializer = self.get_serializer(data={"command_id": command_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = serializer.to_input_dto()

        try:
            command = GetCommandUseCase(DjangoCommandRepository()).execute(dto)
        except ObjectDoesNotExist:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(GetCommandSerializer.to_response(command))
