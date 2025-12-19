# Ubiquitous Language

The following terms must be used consistently across code, documentation, and communication.

---

## Core Terms

- **Livestock**: An individual animal being monitored
- **Device**: A physical sensor or gateway producing telemetry
- **Telemetry**: Raw sensor measurement with timestamp
- **LiveStatus**: Latest known snapshot of telemetry
- **Health**: Evaluated condition derived from telemetry
- **Prediction**: Forward-looking health risk assessment
- **Incident**: A condition requiring attention or action
- **Rule**: Deterministic condition applied to telemetry
- **Edge Node**: On-farm gateway connecting devices to cloud

---

## Explicit Distinctions

- Telemetry ≠ Health  
- Health ≠ Incident  
- LiveStatus ≠ Historical data  
- Rule violation ≠ Incident (incident is a decision)

---

## Forbidden Language

- “Alert” as a domain concept (alerts are UI concerns)
- “Event” for persisted domain state (event ≠ record)
