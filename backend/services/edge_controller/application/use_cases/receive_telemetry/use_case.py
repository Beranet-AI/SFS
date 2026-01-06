from ....domain.exceptions.validation_error import DomainValidationError
from ....domain.repositories.device_registry import DeviceRegistry
from ....domain.specifications.telemetry_payload_specification import (
    TelemetryPayloadSpecification,
)
from ....domain.value_objects.device_id import DeviceId
from ....infrastructure.clients.management_telemetry_client import (
    ManagementTelemetryClient,
)
from .input_dto import ReceiveTelemetryInputDTO
from .output_dto import ReceiveTelemetryOutputDTO


class ReceiveTelemetryUseCase:
    """
    Validate and forward raw telemetry received by the edge.
    """

    def __init__(
        self,
        *,
        device_registry: DeviceRegistry,
        telemetry_client: ManagementTelemetryClient,
        telemetry_specification: TelemetryPayloadSpecification | None = None,
    ) -> None:
        self._device_registry = device_registry
        self._telemetry_client = telemetry_client
        self._telemetry_specification = (
            telemetry_specification or TelemetryPayloadSpecification()
        )

    def execute(
        self, dto: ReceiveTelemetryInputDTO
    ) -> ReceiveTelemetryOutputDTO:
        device_id = DeviceId(dto.device_id)

        if not self._device_registry.is_registered(device_id):
            raise DomainValidationError("Device is not registered")

        self._telemetry_specification.validate(dto.to_payload())
        self._telemetry_client.send_raw_telemetry(dto.to_payload())

        return ReceiveTelemetryOutputDTO(status="ACCEPTED")
