from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SendCommandOutput:
    id: str
    command_name: str
    target_kind: str
    target_id: str
    edge_node_id: str
    payload: Dict[str, Any]
    idempotency_key: str
    status: str
    source: str
    created_by: str
    created_at: str
    ack_deadline_sec: int
    result_deadline_sec: int
    max_attempts: int
    acked_at: str | None
    started_at: str | None
    finished_at: str | None
    last_error_code: str
    last_error_message: str
    last_result: Dict[str, Any]
