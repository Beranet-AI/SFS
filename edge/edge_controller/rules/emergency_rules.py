def emergency_check(reading):
    if reading["metric"] == "temperature" and reading["value"] > 45:
        return {
            "action": "FAN_ON",
            "reason": "Local emergency temperature"
        }
