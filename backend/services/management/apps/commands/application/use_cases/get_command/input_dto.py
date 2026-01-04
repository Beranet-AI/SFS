from dataclasses import dataclass

from shared.schemas.management.commands.get_command.get_command_input import GetCommandInput


@dataclass
class GetCommandInputDTO(GetCommandInput):
    command_id: str
