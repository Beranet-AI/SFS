from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.serializers.ack_command_serializer import AckCommandSerializer
from apps.commands.application.use_cases.ack_command.use_case import (
    AckCommandUseCase,
)
from apps.commands.infrastructure.repositories.command_attempt_repository import (
    DjangoCommandAttemptRepository,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)


class AckCommandView(BaseController):
    """
    POST /commands/ack/
    """

    serializer_class = AckCommandSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = serializer.to_input_dto()
        AckCommandUseCase(
            command_repository=DjangoCommandRepository(),
            attempt_repository=DjangoCommandAttemptRepository(),
        ).execute(dto)

        return Response(AckCommandSerializer.to_response())
