from django.utils import dateparse, timezone

from apps.commands.domain.enums.scan_status import ScanStatus


class ScanResultMapper:
    @staticmethod
    def _parse_datetime(value):
        if not value:
            return None
        if hasattr(value, "tzinfo"):
            return value
        parsed = dateparse.parse_datetime(str(value))
        return parsed or None

    @classmethod
    def to_model_data(cls, payload: dict) -> dict:
        scan_status = payload.get("scan_status")
        if scan_status not in {
            ScanStatus.NEW.value,
            ScanStatus.KNOWN.value,
            ScanStatus.CHANGED.value,
        }:
            scan_status = ScanStatus.NEW.value

        last_seen_at = cls._parse_datetime(payload.get("last_seen_at"))
        discovered_at = cls._parse_datetime(payload.get("discovered_at"))
        if discovered_at is None:
            discovered_at = timezone.now()

        raw_capabilities = payload.get("raw_capabilities")
        if raw_capabilities is None:
            raw_capabilities = payload.get("capabilities")

        return {
            "device_uid": str(
                payload.get("device_uid")
                or payload.get("device_id")
                or payload.get("serial")
                or ""
            ),
            "device_name": payload.get("device_name"),
            "device_category": payload.get("device_category") or "",
            "device_type": payload.get("device_type") or "",
            "protocol": payload.get("protocol") or "",
            "adapter_type": payload.get("adapter_type") or "",
            "direction": payload.get("direction") or "uplink_only",
            "supports_commands": bool(payload.get("supports_commands")),
            "supported_command_categories": payload.get(
                "supported_command_categories", []
            )
            or [],
            "ip_address": payload.get("ip_address"),
            "port": payload.get("port"),
            "network_address": payload.get("network_address"),
            "signal_strength": payload.get("signal_strength"),
            "firmware_version": payload.get("firmware_version"),
            "vendor": payload.get("vendor"),
            "model": payload.get("model"),
            "battery_level": payload.get("battery_level"),
            "last_seen_at": last_seen_at,
            "discovered_at": discovered_at,
            "scan_status": scan_status,
            "raw_capabilities": raw_capabilities,
        }
