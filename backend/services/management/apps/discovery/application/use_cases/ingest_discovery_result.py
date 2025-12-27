from apps.discovery.models import DeviceDiscoveryModel


class IngestDiscoveryResultUseCase:

    def execute(self, *, payload: dict):
        DeviceDiscoveryModel.objects.update_or_create(
            device_serial=payload["device_serial"],
            defaults={
                "ip_address": payload.get("ip_address"),
                "protocol": payload.get("protocol", "unknown"),
                "raw_payload": payload,
            },
        )
