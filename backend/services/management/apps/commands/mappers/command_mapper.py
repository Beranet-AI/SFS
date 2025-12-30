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
        return {
            "id": str(command.id),
            "command_name": command.command_name,
            "target_kind": command.target_kind,
            "target_id": command.target_id,
            "edge_node_id": command.edge_node_id,
            "payload": command.payload,
            "idempotency_key": command.idempotency_key,
            "status": command.status,
            "source": command.source,
            "created_by": command.created_by,
            "created_at": (
                command.created_at.isoformat() if command.created_at else None
            ),
            "ack_deadline_sec": command.ack_deadline_sec,
            "result_deadline_sec": command.result_deadline_sec,
            "max_attempts": command.max_attempts,
            "acked_at": command.acked_at.isoformat() if command.acked_at else None,
            "started_at": command.started_at.isoformat() if command.started_at else None,
            "finished_at": (
                command.finished_at.isoformat() if command.finished_at else None
            ),
            "last_error_code": command.last_error_code,
            "last_error_message": command.last_error_message,
            "last_result": command.last_result,
        }

    @staticmethod
    def to_ok_response() -> dict:
        return {"ok": True}
