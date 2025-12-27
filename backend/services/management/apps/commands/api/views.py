from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.commands.api.serializers import (
    CommandCreateSerializer,
    CommandSerializer,
    CommandAckSerializer,
    CommandResultSerializer,
)
from apps.commands.application.services.command_api_service import (
    CommandApiService,
)


class CommandCreateView(APIView):
    """
    POST /commands/
    (used for manual control, rules, AI, etc.)
    """

    def post(self, request):
        ser = CommandCreateSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        service = CommandApiService()
        cmd = service.create_command(
            data=ser.validated_data,
            created_by=str(getattr(request.user, "username", "")),
        )

        return Response(
            CommandSerializer(cmd).data,
            status=status.HTTP_201_CREATED,
        )


class CommandDetailView(APIView):
    """
    GET /commands/{id}/
    """

    def get(self, request, command_id):
        service = CommandApiService()
        try:
            cmd = service.get_command(command_id=command_id)
        except Exception:
            return Response(
                {"detail": "not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(CommandSerializer(cmd).data)


class CommandAckView(APIView):
    """
    POST /commands/ack/
    """

    def post(self, request):
        ser = CommandAckSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        service = CommandApiService()
        service.ack_command(data=ser.validated_data)

        return Response({"ok": True})


class CommandResultView(APIView):
    """
    POST /commands/result/
    """

    def post(self, request):
        ser = CommandResultSerializer(data=request.data or {})
        ser.is_valid(raise_exception=True)

        service = CommandApiService()
        service.report_result(data=ser.validated_data)

        return Response({"ok": True})
