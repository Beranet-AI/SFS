# Assumptions & Constraints

---

## Assumptions
- Farms have stable local networks
- Edge nodes can preprocess telemetry
- Operators access system via modern browsers

---

## Constraints
- Management service is the only persistent store
- FastAPI services remain stateless
- Real-time guarantees are best-effort, not hard real-time

---

## Architectural Constraints
- Clean Architecture principles must be followed
- DDD boundaries must be respected
- Shared kernel remains minimal
