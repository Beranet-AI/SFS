from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
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

    serializer_class = ReceiveResultSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = serializer.to_input_dto()
        ReceiveResultUseCase().execute(dto)

        return Response(ReceiveResultSerializer.to_response())
