
---

## `docs/05_api/management/devices_api.md`

```md
# Devices API

Base Path: `/api/v1/devices/`

---

## POST /devices/register/
Registers a new device discovered by edge.

**Request**
```json
{
  "device_id": "dev-9",
  "type": "temperature",
  "livestock_id": "cow-42"
}

GET /devices/
Lists devices and associations.

Mapping

Aggregate: Device
Context: Edge / Devices
Tests: test_devices_api.py