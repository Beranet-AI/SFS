from dataclasses import dataclass
from typing import Any, Dict

from apps.commands.schemas.command.send_command_input import SendCommandInput


@dataclass
class SendCommandInputDTO(SendCommandInput):
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
