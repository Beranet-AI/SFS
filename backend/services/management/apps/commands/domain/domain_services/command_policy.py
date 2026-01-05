from apps.commands.domain.repositories.capability_repository import CapabilityRepository


class CommandPolicy:
    DEFAULT_ACK_DEADLINE_SEC = 10
    DEFAULT_RESULT_DEADLINE_SEC = 60
    DEFAULT_MAX_ATTEMPTS = 5

    def __init__(self, *, capability_repository: CapabilityRepository) -> None:
        self._capability_repository = capability_repository

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
        command_type: str | None = None,
        device_category: str | None = None,
        device_type: str | None = None,
    ) -> dict:
        adapter_type = None
        if command_type and device_category and device_type:
            for capability in self._capability_repository.list_capabilities():
                if (
                    capability.command_type == command_type
                    and capability.device_category == device_category
                    and capability.device_type == device_type
                ):
                    adapter_type = capability.adapter_type
                    break

        payload_value = payload or {}
        if adapter_type:
            payload_value = {**payload_value, "adapter_type": adapter_type}

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
