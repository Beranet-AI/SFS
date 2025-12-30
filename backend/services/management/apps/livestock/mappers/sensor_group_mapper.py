from apps.livestock.application.use_cases.register_sensor_group.input_dto import (
    RegisterLivestockSensorGroupInputDTO,
)
from apps.livestock.application.use_cases.register_sensor_group.output_dto import (
    RegisterLivestockSensorGroupOutputDTO,
)


class LivestockSensorGroupMapper:
    @staticmethod
    def from_payload(payload: dict) -> RegisterLivestockSensorGroupInputDTO:
        return RegisterLivestockSensorGroupInputDTO(
            livestock_id=payload["livestock_id"],
            rfid_device_id=payload["rfid_device_id"],
            sensor_device_ids=payload.get("sensor_device_ids", []),
        )

    @staticmethod
    def to_response(dto: RegisterLivestockSensorGroupOutputDTO) -> dict:
        return {
            "group_id": dto.group_id,
            "livestock_id": dto.livestock_id,
            "rfid_device_id": dto.rfid_device_id,
            "sensor_device_ids": dto.sensor_device_ids,
        }
