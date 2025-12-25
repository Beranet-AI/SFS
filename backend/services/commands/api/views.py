import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.commands.infrastructure.models.command_model import (
    CommandModel,
    CommandStatus,
)
from .serializers import CommandSerializer, CommandCreateSerializer


EDGE_CONTROLLER_BASE_URL = "http://edge_controller:8003"


@api_view(["GET"])
def list_commands(request):
    qs = CommandModel.objects.all().order_by("-created_at")
    return Response(CommandSerializer(qs, many=True).data)


@api_view(["POST"])
def send_command(request):
    ser = CommandCreateSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    data = ser.validated_data

    cmd = CommandModel.objects.create(
        command_type=data["command_type"],
        target_device_serial=data["target_device_serial"],
        params=data.get("params", {}),
        source=data.get("source", "manual"),
        issued_by=request.user.username if request.user.is_authenticated else "system",
    )

    # Forward to edge controller
    try:
        requests.post(
            f"{EDGE_CONTROLLER_BASE_URL}/edge/commands/execute",
            json={
                "command_id": str(cmd.id),
                "command_type": cmd.command_type,
                "target_device_serial": cmd.target_device_serial,
                "params": cmd.params,
            },
            timeout=3,
        )
        cmd.status = CommandStatus.SENT
        cmd.save(update_fields=["status", "updated_at"])
    except Exception as e:
        cmd.status = CommandStatus.FAILED
        cmd.save(update_fields=["status", "updated_at"])
        return Response(
            {"detail": "Failed to send command to edge"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(CommandSerializer(cmd).data, status=status.HTTP_201_CREATED)
