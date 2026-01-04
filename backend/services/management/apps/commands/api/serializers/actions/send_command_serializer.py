from rest_framework import serializers

from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.output_dto import (
    SendCommandOutputDTO,
)
from apps.commands.domain.entities.command import Command
from apps.commands.domain.enums.command_target_kind import CommandTargetKind


def command_to_output(command: Command) -> dict:
    return {
        "id": command.id,
        "command_name": command.command_name,
        "target_kind": command.target_kind.value,
        "target_id": command.target_id,
        "edge_node_id": command.edge_node_id,
        "payload": command.payload,
        "idempotency_key": command.idempotency_key,
        "status": command.status.value,
        "source": command.source,
        "created_by": command.created_by,
        "created_at": command.created_at.isoformat() if command.created_at else None,
        "ack_deadline_sec": command.ack_deadline_sec,
        "result_deadline_sec": command.result_deadline_sec,
        "max_attempts": command.max_attempts,
        "acked_at": command.acked_at.isoformat() if command.acked_at else None,
        "started_at": command.started_at.isoformat() if command.started_at else None,
        "finished_at": command.finished_at.isoformat() if command.finished_at else None,
        "last_error_code": command.last_error_code,
        "last_error_message": command.last_error_message,
        "last_result": command.last_result or {},
    }


class SendCommandSerializer(serializers.Serializer):
    command_name = serializers.CharField(max_length=120)
    target_kind = serializers.ChoiceField(
        choices=[(kind.value, kind.value) for kind in CommandTargetKind]
    )
    target_id = serializers.CharField(max_length=64)
    edge_node_id = serializers.CharField(max_length=64, required=False, allow_blank=True)
    payload = serializers.JSONField(required=False)
    idempotency_key = serializers.CharField(
        max_length=128, required=False, allow_blank=True
    )
    ack_deadline_sec = serializers.IntegerField(required=False, min_value=1)
    result_deadline_sec = serializers.IntegerField(required=False, min_value=1)
    max_attempts = serializers.IntegerField(required=False, min_value=1)
    backoff_sec = serializers.IntegerField(required=False, min_value=0)

    def to_input_dto(self) -> SendCommandInputDTO:
        return SendCommandInputDTO(**self.validated_data)

    @staticmethod
    def to_output_dto(command: Command) -> SendCommandOutputDTO:
        payload = command_to_output(command)
        return SendCommandOutputDTO(**payload)

    @staticmethod
    def to_response(command: Command) -> dict:
        return command_to_output(command)
