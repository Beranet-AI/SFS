from dataclasses import dataclass

from apps.commands.domain.enums.command_status import CommandStatus


@dataclass
class SendCommandOutputDTO:
    command_id: str
    status: CommandStatus
    command_name: str
    target_kind: str
    target_id: str
    edge_node_id: str
