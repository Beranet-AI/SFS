from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.serializers.receive_result_serializer import (
    ReceiveResultSerializer,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.application.services.discovery_result_service import (
    DiscoveryResultService,
)
from apps.commands.infrastructure.repositories.command_attempt_repository import (
    DjangoCommandAttemptRepository,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from apps.commands.infrastructure.repositories.discovered_device_repository import (
    DjangoDiscoveredDeviceRepository,
)
from apps.commands.infrastructure.repositories.discovery_session_repository import (
    DjangoDiscoverySessionRepository,
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
        ReceiveResultUseCase(
            command_repository=DjangoCommandRepository(),
            attempt_repository=DjangoCommandAttemptRepository(),
            discovery_result_service=DiscoveryResultService(
                session_repository=DjangoDiscoverySessionRepository(),
                device_repository=DjangoDiscoveredDeviceRepository(),
            ),
        ).execute(dto)

        return Response(ReceiveResultSerializer.to_response())
