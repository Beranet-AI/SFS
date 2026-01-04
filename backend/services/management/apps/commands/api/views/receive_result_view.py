from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.forms.receive_result_form import ReceiveResultForm
from apps.commands.api.serializers.receive_result_serializer import (
    ReceiveResultSerializer,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)


class ReceiveResultView(BaseController):
    """
    POST /commands/result/
    """

    def post(self, request):
        form = ReceiveResultForm(request.data or {})
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = ReceiveResultSerializer.to_input_dto(form.cleaned_data)
        ReceiveResultUseCase().execute(dto)

        return Response(ReceiveResultSerializer.to_response())
