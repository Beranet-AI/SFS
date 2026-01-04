from apps.commands.domain.value_objects.command_payload import CommandPayload


class CommandPolicy:
    DEFAULT_ACK_DEADLINE_SEC = 10
    DEFAULT_RESULT_DEADLINE_SEC = 60
    DEFAULT_MAX_ATTEMPTS = 5

    def apply(
        self,
        *,
        command_name: str,
        target_kind: str,
        target_id: str,
        edge_node_id: str | None,
        payload: dict | None,
        idempotency_key: str | None,
        ack_deadline_sec: int | None,
        result_deadline_sec: int | None,
        max_attempts: int | None,
    ) -> dict:
        payload_value = CommandPayload.from_raw(payload).data
        return {
            "command_name": command_name,
            "target_kind": target_kind,
            "target_id": target_id,
            "edge_node_id": edge_node_id or "",
            "payload": payload_value,
            "idempotency_key": idempotency_key or "",
            "ack_deadline_sec": ack_deadline_sec or self.DEFAULT_ACK_DEADLINE_SEC,
            "result_deadline_sec": result_deadline_sec
            or self.DEFAULT_RESULT_DEADLINE_SEC,
            "max_attempts": max_attempts or self.DEFAULT_MAX_ATTEMPTS,
        }
