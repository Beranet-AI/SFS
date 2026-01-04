from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.serializers.ack_command_serializer import AckCommandSerializer
from apps.commands.application.use_cases.ack_command.use_case import (
    AckCommandUseCase,
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
        AckCommandUseCase().execute(dto)

        return Response(AckCommandSerializer.to_response())
