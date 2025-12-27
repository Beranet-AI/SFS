from django.db import transaction
from django.utils import timezone

from apps.discovery.models import DeviceDiscoveryModel, DiscoveryStatus
from apps.devices.models import DeviceModel
from apps.discovery.domain.events.device_promoted import DevicePromoted
from apps.discovery.domain.events.publisher import DomainEventPublisher


class ApproveAndPromoteDeviceUseCase:
    """
    Atomic use case:
    Discovery (PENDING) -> Device + Discovery(APPROVED)
    + Domain Event: DevicePromoted
    """

    def __init__(self):
        self.publisher = DomainEventPublisher()

    @transaction.atomic
    def execute(self, *, discovery_id):
        discovery = (
            DeviceDiscoveryModel.objects
            .select_for_update()
            .get(id=discovery_id)
        )

        if discovery.status != DiscoveryStatus.PENDING:
            raise ValueError("Discovery is not in PENDING state")

        device = DeviceModel.objects.create(
            device_serial=discovery.device_serial,
            device_type=discovery.device_type,
            display_name=discovery.display_name,
            role=discovery.role,
            protocol=discovery.protocol,
            manufacturer=discovery.manufacturer,
            model=discovery.model,
            firmware=discovery.firmware,
            capabilities=discovery.capabilities,
            status=DeviceModel.Status.ACTIVE,
            last_seen_at=discovery.last_seen_at,
        )

        discovery.status = DiscoveryStatus.APPROVED
        discovery.approved_at = timezone.now()
        discovery.save(update_fields=["status", "approved_at"])

        # ---------- DOMAIN EVENT ----------
        event = DevicePromoted(
            discovery_id=discovery.id,
            device_id=device.id,
            device_serial=discovery.device_serial,
            occurred_at=timezone.now(),
        )

        self.publisher.publish(event)

        return device
