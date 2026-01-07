import uuid

from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.enums.command_category import CommandCategory
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.enums.device_category import DeviceCategory
from apps.commands.domain.enums.device_type import DeviceType
from apps.commands.domain.exceptions.invalid_target import InvalidTargetError

from .input_dto import StartNetworkScanInputDTO
from .output_dto import StartNetworkScanOutputDTO


class StartNetworkScanUseCase:
    """
    Use case responsible for starting a network discovery process
    on a specific edge controller.
    """

    def __init__(self, *, send_command_use_case: SendCommandUseCase) -> None:
        self._send_command_use_case = send_command_use_case

    def execute(
        self,
        dto: StartNetworkScanInputDTO,
        *,
        created_by: str,
    ) -> StartNetworkScanOutputDTO:
        if not dto.edge_node_id:
            raise InvalidTargetError(
                "edge_node_id is required to start network scan"
            )

        scan_id = str(uuid.uuid4())

        send_command_output = self._send_command_use_case.execute(
            SendCommandInputDTO(
                command_name=CommandType.GET_CONNECTED_DEVICES.value,
                command_type=CommandType.DISCOVER.value,
                command_category=CommandCategory.QUERY.value,
                target_kind="edge_node",
                target_id=dto.edge_node_id,
                edge_node_id=dto.edge_node_id,
                payload={
                    "scan_id": scan_id,
                    "initiated_by": created_by,
                },
                idempotency_key=scan_id,
                device_category=DeviceCategory.INFRASTRUCTURE.value,
                device_type=DeviceType.EDGE_CONTROLLER.value,
            ),
            created_by=created_by,
        )

        return StartNetworkScanOutputDTO(
            scan_id=scan_id,
            command_id=send_command_output.command_id,
        )
