from dataclasses import dataclass

from apps.commands.domain.entities.command import Command


@dataclass
class GetCommandOutputDTO:
    command: Command
