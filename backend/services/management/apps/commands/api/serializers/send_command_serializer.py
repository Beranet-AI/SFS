from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.output_dto import (
    SendCommandOutputDTO,
)
from apps.commands.domain.entities.command import Command


def _command_to_output(command: Command) -> dict:
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


class SendCommandSerializer:
    @staticmethod
    def to_input_dto(data: dict) -> SendCommandInputDTO:
        return SendCommandInputDTO(**data)

    @staticmethod
    def to_output_dto(command: Command) -> SendCommandOutputDTO:
        payload = _command_to_output(command)
        return SendCommandOutputDTO(**payload)

    @staticmethod
    def to_response(command: Command) -> dict:
        return _command_to_output(command)
