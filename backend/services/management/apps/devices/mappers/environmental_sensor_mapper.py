from apps.devices.application.use_cases.register_environmental_sensor.input_dto import (
    RegisterEnvironmentalSensorInputDTO,
)
from apps.devices.application.use_cases.register_environmental_sensor.output_dto import (
    RegisterEnvironmentalSensorOutputDTO,
)


class EnvironmentalSensorMapper:
    @staticmethod
    def from_payload(payload: dict) -> RegisterEnvironmentalSensorInputDTO:
        return RegisterEnvironmentalSensorInputDTO(
            serial=payload["serial"],
            device_type=payload["device_type"],
            json_schema=payload["json_schema"],
            raw_example=payload["raw_example"],
            farm_id=payload["farm_id"],
            barn_id=payload["barn_id"],
            zone_id=payload["zone_id"],
            created_by=payload["created_by"],
            approved_by=payload["approved_by"],
            display_name=payload.get("display_name"),
            metadata=payload.get("metadata"),
            capabilities=payload.get("capabilities"),
            kind=payload.get("kind"),
        )

    @staticmethod
    def to_response(dto: RegisterEnvironmentalSensorOutputDTO) -> dict:
        return {
            "device_id": dto.device_id,
            "serial": dto.serial,
            "schema_id": dto.schema_id,
            "schema_version": dto.schema_version,
        }
