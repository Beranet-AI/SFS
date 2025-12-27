from apps.discovery.domain.events.device_promoted import DevicePromoted


def handle_device_promoted(event: DevicePromoted):
    print(
        f"[DOMAIN EVENT] DevicePromoted | "
        f"discovery={event.discovery_id} "
        f"device={event.device_id} "
        f"serial={event.device_serial}"
    )
