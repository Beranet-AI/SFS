from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SendCommandInput:
    command_name: str
    target_kind: str
    target_id: str
    edge_node_id: str | None = None
    payload: Dict[str, Any] | None = None
    idempotency_key: str | None = None
    ack_deadline_sec: int | None = None
    result_deadline_sec: int | None = None
    max_attempts: int | None = None
    backoff_sec: int | None = None

    def to_dict(self) -> dict:
        data = {
            "command_name": self.command_name,
            "target_kind": self.target_kind,
            "target_id": self.target_id,
            "edge_node_id": self.edge_node_id,
            "payload": self.payload,
            "idempotency_key": self.idempotency_key,
            "ack_deadline_sec": self.ack_deadline_sec,
            "result_deadline_sec": self.result_deadline_sec,
            "max_attempts": self.max_attempts,
            "backoff_sec": self.backoff_sec,
        }

        return {key: value for key, value in data.items() if value is not None}
