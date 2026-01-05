from apps.commands.application.use_cases.send_command.output_dto import (
    SendCommandOutputDTO,
)
from apps.commands.application.use_cases.start_network_scan.input_dto import (
    StartNetworkScanInputDTO,
)
from apps.commands.application.use_cases.start_network_scan.use_case import (
    StartNetworkScanUseCase,
)
from apps.commands.domain.enums.command_status import CommandStatus


class FakeSendCommandUseCase:
    def __init__(self):
        self.last_dto = None

    def execute(self, dto, *, created_by: str):
        self.last_dto = dto
        return SendCommandOutputDTO(
            command_id="cmd-123",
            status=CommandStatus.DISPATCHED,
            command_name=dto.command_name,
            target_kind=dto.target_kind,
            target_id=dto.target_id,
            edge_node_id=dto.edge_node_id or "",
        )


def test_start_network_scan_builds_scan_id():
    sender = FakeSendCommandUseCase()
    use_case = StartNetworkScanUseCase(send_command_use_case=sender)

    output = use_case.execute(
        StartNetworkScanInputDTO(edge_node_id="edge-1"),
        created_by="tester",
    )

    assert output.command_id == "cmd-123"
    assert output.scan_id
    assert sender.last_dto.payload["scan_id"] == output.scan_id
