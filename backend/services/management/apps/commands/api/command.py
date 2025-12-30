from rest_framework import status
from rest_framework.response import Response

from apps.commands.api.base import BaseController
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
from apps.commands.models import CommandStatus


class CommandCreateController(BaseController):
    """
    POST /commands/
    (used for manual control, rules, AI, etc.)
    """

    def post(self, request):
        payload = request.data or {}
        try:
            self.require_fields(
                payload,
                [
                    "command_name",
                    "target_kind",
                    "target_id",
                ],
            )

            inbound = InboundCommandMapper.from_create_payload(payload)
            cmd = SendCommandUseCase().create_command(
                inbound,
                created_by=self.get_username(request),
            )

            return Response(
                OutboundCommandMapper.to_response(cmd),
                status=status.HTTP_201_CREATED,
            )
        except KeyError as exc:
            return Response(
                {"detail": f"missing field(s): {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommandDetailController(BaseController):
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


class CommandAckController(BaseController):
    """
    POST /commands/ack/
    """

    def post(self, request):
        payload = request.data or {}
        try:
            self.require_fields(payload, ["command_id", "attempt_no"])

            inbound = InboundCommandMapper.from_ack_payload(payload)
            SendCommandUseCase().ack_command(data=inbound)

            return Response(OutboundCommandMapper.to_ok_response())
        except KeyError as exc:
            return Response(
                {"detail": f"missing field(s): {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommandResultController(BaseController):
    """
    POST /commands/result/
    """

    def post(self, request):
        payload = request.data or {}
        try:
            self.require_fields(payload, ["command_id", "attempt_no", "status"])
            allowed_statuses = {
                CommandStatus.SUCCEEDED,
                CommandStatus.FAILED,
                CommandStatus.TIMED_OUT,
                CommandStatus.CANCELLED,
            }
            if payload.get("status") not in allowed_statuses:
                return Response(
                    {"detail": "invalid status"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            inbound = InboundResultMapper.from_payload(payload)
            ReceiveResultUseCase().report(inbound)

            return Response(
                OutboundResultMapper.to_response(ReceiveResultOutputDTO(ok=True))
            )
        except KeyError as exc:
            return Response(
                {"detail": f"missing field(s): {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
