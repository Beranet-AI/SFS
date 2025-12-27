from django.contrib import admin, messages

from apps.discovery.models import DeviceDiscoveryModel, DiscoveryStatus
from apps.discovery.application.use_cases.approve_and_promote_device import (
    ApproveAndPromoteDeviceUseCase,
)


@admin.action(description="Approve & Promote to Device")
def approve_and_promote(modeladmin, request, queryset):
    use_case = ApproveAndPromoteDeviceUseCase()
    success = 0
    failed = 0

    for discovery in queryset:
        if discovery.status != DiscoveryStatus.PENDING:
            failed += 1
            continue

        try:
            use_case.execute(discovery_id=discovery.id)
            success += 1
        except Exception:
            failed += 1

    if success:
        messages.success(
            request,
            f"{success} device(s) successfully approved and promoted."
        )
    if failed:
        messages.error(
            request,
            f"{failed} device(s) failed to promote."
        )


@admin.register(DeviceDiscoveryModel)
class DeviceDiscoveryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_serial",
        "device_type",
        "status",
        "approved_at",
        "last_seen_at",
    )

    list_filter = (
        "status",
        "device_type",
    )

    actions = [approve_and_promote]
