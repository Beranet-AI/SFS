
from typing import Literal
from datetime import datetime, timezone

from ...logging import get_logger

logger = get_logger(__name__)


class DeviceClient:
    """
    Infrastructure adapter for communicating with edge devices.
    For now, acts as a stub / mock implementation.
    """

    def send_on_off(
        self,
        *,
        device_id: str,
        action: Literal["ON", "OFF"],
    ) -> bool:
        """
        Send ON / OFF command to a device.

        Returns:
            bool: True if command was accepted, False otherwise
        """

        logger.info(
            "Sending ON_OFF command",
            extra={
                "device_id": device_id,
                "action": action,
                "sent_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        # TODO: replace with real MQTT publish
        return True

    def send_reboot(self, device_id: str) -> bool:
        """
        Send REBOOT command to a device
        """

        logger.info(
            "Sending REBOOT command",
            extra={
                "device_id": device_id,
                "sent_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        # TODO: replace with real MQTT publish
        return True
