from apps.devices.application.use_cases.register_control_device.input_dto import (
    RegisterControlDeviceInputDTO,
)
from apps.devices.application.use_cases.register_control_device.output_dto import (
    RegisterControlDeviceOutputDTO,
)


class ControlDeviceMapper:
    @staticmethod
    def from_payload(payload: dict) -> RegisterControlDeviceInputDTO:
        return RegisterControlDeviceInputDTO(
            serial=payload["serial"],
            farm_id=payload["farm_id"],
            barn_id=payload["barn_id"],
            zone_id=payload["zone_id"],
            created_by=payload["created_by"],
            display_name=payload.get("display_name"),
            metadata=payload.get("metadata"),
            capabilities=payload.get("capabilities"),
            kind=payload.get("kind"),
        )

    @staticmethod
    def to_response(dto: RegisterControlDeviceOutputDTO) -> dict:
        return {
            "device_id": dto.device_id,
            "serial": dto.serial,
        }
