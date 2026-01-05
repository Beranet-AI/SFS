from apps.commands.domain.enums.scan_status import ScanStatus


class ScanResultMapper:
    @staticmethod
    def to_model_data(payload: dict) -> dict:
        scan_status = payload.get("scan_status")
        status = "new"
        if scan_status in {ScanStatus.KNOWN.value, ScanStatus.CHANGED.value}:
            status = "new"

        capabilities = {
            "supported_command_categories": payload.get(
                "supported_command_categories", []
            ),
            "adapter_type": payload.get("adapter_type"),
            "protocol": payload.get("protocol"),
        }

        return {
            "device_id": str(
                payload.get("device_uid")
                or payload.get("device_id")
                or payload.get("serial")
                or ""
            ),
            "device_type": payload.get("device_type") or "",
            "ip_address": payload.get("ip_address") or payload.get("ip") or "",
            "capabilities": capabilities,
            "raw_payload": payload,
            "status": status,
        }
