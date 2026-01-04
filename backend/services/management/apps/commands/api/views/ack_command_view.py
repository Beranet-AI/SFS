from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.forms.ack_command_form import AckCommandForm
from apps.commands.api.serializers.ack_command_serializer import AckCommandSerializer
from apps.commands.application.use_cases.ack_command.use_case import (
    AckCommandUseCase,
)


class AckCommandView(BaseController):
    """
    POST /commands/ack/
    """

    def post(self, request):
        form = AckCommandForm(request.data or {})
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = AckCommandSerializer.to_input_dto(form.cleaned_data)
        AckCommandUseCase().execute(dto)

        return Response(AckCommandSerializer.to_response())
