from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from apps.commands.api.base import BaseController
from apps.commands.api.serializers.actions.send_command_serializer import (
    SendCommandSerializer,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)


class SendCommandView(BaseController):
    """
    GET /commands/
    POST /commands/
    """

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = SendCommandSerializer
    template_name = "management/commands/actions/send_command.html"

    def get(self, request):
        serializer = self.get_serializer()
        return Response(
            {"serializer": serializer},
            template_name=self.template_name,
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if request.accepted_renderer.format == "html":
                return Response(
                    {"serializer": serializer},
                    status=status.HTTP_400_BAD_REQUEST,
                    template_name=self.template_name,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = serializer.to_input_dto()
        command = SendCommandUseCase(
            repository=DjangoCommandRepository(),
            edge_client=EdgeControllerClient(),
        ).execute(dto, created_by=self.get_username(request))
        response_payload = SendCommandSerializer.to_response(command)

        if request.accepted_renderer.format == "html":
            return Response(
                {
                    "command": response_payload,
                    "serializer": self.get_serializer(),
                },
                status=status.HTTP_201_CREATED,
                template_name="management/commands/actions/send_command_result.html",
            )

        return Response(response_payload, status=status.HTTP_201_CREATED)
