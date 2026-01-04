from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.domain.value_objects.retry_policy import RetryPolicy


@dataclass
class Command:
    id: str
    command_name: str
    target_kind: CommandTargetKind
    target_id: str
    edge_node_id: str
    payload: Dict[str, Any]
    idempotency_key: str
    status: CommandStatus
    source: str
    created_by: str
    created_at: datetime
    ack_deadline_sec: int
    result_deadline_sec: int
    max_attempts: int
    acked_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    last_error_code: str = ""
    last_error_message: str = ""
    last_result: Dict[str, Any] | None = None
    retry_policy: RetryPolicy | None = None
