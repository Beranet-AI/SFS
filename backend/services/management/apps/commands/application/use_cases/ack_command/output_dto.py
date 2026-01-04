from dataclasses import dataclass

from shared.schemas.ack_command.ack_command_output import AckCommandOutput


@dataclass
class AckCommandOutputDTO(AckCommandOutput):
    ok: bool
