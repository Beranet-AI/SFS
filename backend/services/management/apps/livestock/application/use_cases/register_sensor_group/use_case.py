from django.db import transaction

from apps.devices.application.services.device_service import DeviceService
from apps.devices.models import DeviceModel
from apps.livestock.application.use_cases.register_sensor_group.input_dto import (
    RegisterLivestockSensorGroupInputDTO,
)
from apps.livestock.application.use_cases.register_sensor_group.output_dto import (
    RegisterLivestockSensorGroupOutputDTO,
)
from apps.livestock.models import LivestockModel, LivestockSensorGroupModel


class RegisterLivestockSensorGroupUseCase:
    def __init__(self, device_service: DeviceService | None = None) -> None:
        self._device_service = device_service or DeviceService()

    @transaction.atomic
    def execute(
        self, input_dto: RegisterLivestockSensorGroupInputDTO
    ) -> RegisterLivestockSensorGroupOutputDTO:
        livestock = LivestockModel.objects.get(id=input_dto.livestock_id)
        rfid_device = DeviceModel.objects.get(id=input_dto.rfid_device_id)

        sensor_ids = {
            str(device_id) for device_id in input_dto.sensor_device_ids
        }
        sensor_ids.add(str(rfid_device.id))

        sensors = list(DeviceModel.objects.filter(id__in=sensor_ids))
        found_ids = {str(device.id) for device in sensors}
        missing_ids = sensor_ids - found_ids
        if missing_ids:
            raise ValueError(
                "Unknown sensor device IDs: "
                + ", ".join(sorted(missing_ids))
            )

        group, _ = LivestockSensorGroupModel.objects.update_or_create(
            livestock=livestock,
            defaults={
                "rfid_device": rfid_device,
            },
        )
        group.sensors.set(sensors)

        for device in sensors:
            self._device_service.assign(
                device=device,
                livestock_id=str(livestock.id),
            )

        return RegisterLivestockSensorGroupOutputDTO(
            group_id=str(group.id),
            livestock_id=str(livestock.id),
            rfid_device_id=str(rfid_device.id),
            sensor_device_ids=[str(device.id) for device in sensors],
        )
