from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.forms.get_command_form import GetCommandForm
from apps.commands.api.serializers.get_command_serializer import GetCommandSerializer
from apps.commands.application.use_cases.get_command.use_case import (
    GetCommandUseCase,
)


class GetCommandView(BaseController):
    """
    GET /commands/{id}/
    """

    def get(self, request, command_id):
        form = GetCommandForm({"command_id": command_id})
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = GetCommandSerializer.to_input_dto(form.cleaned_data)

        try:
            command = GetCommandUseCase().execute(dto)
        except ObjectDoesNotExist:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(GetCommandSerializer.to_response(command))
