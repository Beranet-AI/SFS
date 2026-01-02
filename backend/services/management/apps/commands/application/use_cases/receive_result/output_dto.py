from dataclasses import dataclass


from shared.schemas.management.commands.receive_result.receive_result_output import ReceiveResultOutput



@dataclass
class ReceiveResultOutputDTO(ReceiveResultOutput):
    ok: bool
