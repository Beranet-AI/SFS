# Scaling Strategy

SFS is designed to scale incrementally.

---

## Horizontal Scaling

Stateless services:
- data_ingestion
- monitoring
- ai_decision
- edge_controller

Can be scaled horizontally.

---

## Vertical Scaling

- Management service (CPU/RAM)
- PostgreSQL database

---

## Bottleneck Identification

Key metrics:
- Telemetry ingestion rate
- API response time
- Incident creation latency

---

## Scaling Scenarios

### High Telemetry Volume
- Scale data_ingestion horizontally
- Increase DB write capacity

---

### High Read Load
- Scale monitoring service
- Add caching layer

---

### AI Load Increase
- Scale ai_decision independently
- Queue-based evaluation (future)

---

## Non-Goals

- Automatic auto-scaling (initially)
- Premature optimization
