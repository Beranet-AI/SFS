from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.forms.send_command_form import SendCommandForm
from apps.commands.api.serializers.send_command_serializer import SendCommandSerializer
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)


class SendCommandView(BaseController):
    """
    POST /commands/
    """

    def post(self, request):
        form = SendCommandForm(request.data or {})
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = SendCommandSerializer.to_input_dto(form.cleaned_data)
        command = SendCommandUseCase().execute(
            dto,
            created_by=self.get_username(request),
        )

        return Response(
            SendCommandSerializer.to_response(command),
            status=status.HTTP_201_CREATED,
        )
