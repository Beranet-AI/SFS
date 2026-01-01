from dataclasses import dataclass


from backend.shared.schemas.management.commands.result.receive_result_output import ReceiveResultOutput



@dataclass
class ReceiveResultOutputDTO(ReceiveResultOutput):
    ok: bool
