class SensorGatewayClient:
    """
    خروج از bounded context: دریافت داده‌های سنسور (در صورت نیاز)
    """
    def fetch_latest_zone_metrics(self, zone_id: str) -> dict:
        # Stub
        return {"zone_id": zone_id, "temperature": None, "humidity": None, "ammonia": None}
