from apps.commands.api.serializers import CommandSerializer
from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)


class InboundCommandMapper:
    @staticmethod
    def from_create_payload(payload: dict) -> SendCommandInputDTO:
        return SendCommandInputDTO(
            command_name=payload["command_name"],
            target_kind=payload["target_kind"],
            target_id=payload["target_id"],
            edge_node_id=payload.get("edge_node_id"),
            payload=payload.get("payload"),
            idempotency_key=payload.get("idempotency_key"),
            ack_deadline_sec=payload.get("ack_deadline_sec"),
            result_deadline_sec=payload.get("result_deadline_sec"),
            max_attempts=payload.get("max_attempts"),
            backoff_sec=payload.get("backoff_sec"),
        )

    @staticmethod
    def from_ack_payload(payload: dict) -> dict:
        return dict(payload)

    @staticmethod
    def from_command_id(command_id: str) -> str:
        return command_id


class OutboundCommandMapper:
    @staticmethod
    def to_response(command) -> dict:
        return CommandSerializer(command).data

    @staticmethod
    def to_ok_response() -> dict:
        return {"ok": True}
