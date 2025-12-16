import uuid
from datetime import datetime

def scan_devices():
    # شبیه‌سازی (بعداً Modbus / network scan)
    return [
        {
            "tempId": str(uuid.uuid4()),
            "hardwareAddress": "28-FF-3A-9C-91-16-04-5B",
            "kind": "sensor",
            "metrics": ["temperature"],
            "protocol": "labview",
            "detectedAt": datetime.utcnow().isoformat(),
        }
    ]
