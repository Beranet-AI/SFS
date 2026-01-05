from dataclasses import dataclass
from typing import Any


@dataclass
class SendCommandInputDTO:
    command_name: str
    target_kind: str
    target_id: str
    edge_node_id: str | None = None
    payload: dict[str, Any] | None = None
    idempotency_key: str | None = None
    ack_deadline_sec: int | None = None
    result_deadline_sec: int | None = None
    max_attempts: int | None = None
    backoff_sec: int | None = None
    command_type: str | None = None
    command_category: str | None = None
    device_category: str | None = None
    device_type: str | None = None
