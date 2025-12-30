from dataclasses import dataclass

from apps.commands.schemas.result.receive_result_output import ReceiveResultOutput


@dataclass
class ReceiveResultOutputDTO(ReceiveResultOutput):
    ok: bool
