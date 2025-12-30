from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.commands.api.serializers import (
    CommandCreateSerializer,
    CommandAckSerializer,
    CommandResultSerializer,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.mappers.command_mapper import (
    InboundCommandMapper,
    OutboundCommandMapper,
)
from apps.commands.mappers.result_mapper import (
    InboundResultMapper,
    OutboundResultMapper,
)
from apps.commands.application.use_cases.receive_result.output_dto import (
    ReceiveResultOutputDTO,
)


class CommandCreateView(APIView):
    """
    POST /commands/
    (used for manual control, rules, AI, etc.)
    """

    def post(self, request):
        ser = CommandCreateSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        inbound = InboundCommandMapper.from_create_payload(ser.validated_data)
        cmd = SendCommandUseCase().create_command(
            inbound,
            created_by=str(getattr(request.user, "username", "")),
        )

        return Response(
            OutboundCommandMapper.to_response(cmd),
            status=status.HTTP_201_CREATED,
        )


class CommandDetailView(APIView):
    """
    GET /commands/{id}/
    """

    def get(self, request, command_id):
        try:
            inbound = InboundCommandMapper.from_command_id(command_id)
            cmd = SendCommandUseCase().get_command(command_id=inbound)
        except Exception:
            return Response(
                {"detail": "not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(OutboundCommandMapper.to_response(cmd))


class CommandAckView(APIView):
    """
    POST /commands/ack/
    """

    def post(self, request):
        ser = CommandAckSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        inbound = InboundCommandMapper.from_ack_payload(ser.validated_data)
        SendCommandUseCase().ack_command(data=inbound)

        return Response(OutboundCommandMapper.to_ok_response())


class CommandResultView(APIView):
    """
    POST /commands/result/
    """

    def post(self, request):
        ser = CommandResultSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        inbound = InboundResultMapper.from_payload(ser.validated_data)
        ReceiveResultUseCase().report(inbound)

        return Response(
            OutboundResultMapper.to_response(ReceiveResultOutputDTO(ok=True))
        )
