from dataclasses import dataclass

from shared.schemas.management.commands.ack_command.ack_command_output import AckCommandOutput


@dataclass
class AckCommandOutputDTO(AckCommandOutput):
    ok: bool
