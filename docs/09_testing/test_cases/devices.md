# Test Cases – Devices & Edge

---

## TC-DEV-01 Register Device

**Given**
- Edge reports a new device

**When**
- Device registration API is called

**Then**
- Device is persisted
- Device type is immutable

**Mapped To**
- API: /devices/register/
- Tests:
  - test_devices_api.py

---

## TC-DEV-02 Associate Device with Livestock

**Given**
- Device exists
- Livestock exists

**When**
- Association is created

**Then**
- Device belongs to livestock
- No telemetry is affected

---

## TC-DEV-03 Edge Heartbeat

**Given**
- Edge node is active

**When**
- Heartbeat is received

**Then**
- Edge status is updated
- No domain state changes

**Mapped To**
- edge_controller tests
