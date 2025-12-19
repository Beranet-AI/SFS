# Bounded Contexts

SFS is decomposed into the following bounded contexts:

---

## 1. Livestock Context
**Responsibility**
- Manage livestock identity and metadata
- Maintain association with farm locations

**Owns**
- Livestock entity
- Livestock location value object

**Does NOT own**
- Telemetry
- Health evaluation logic

**Code Mapping**
- management/apps/livestock/

---

## 2. Telemetry Context
**Responsibility**
- Store and expose raw telemetry data
- Maintain immutable historical records

**Owns**
- Telemetry records
- Telemetry ingestion interfaces

**Does NOT own**
- Health decisions
- Incident creation

**Code Mapping**
- management/apps/telemetry/
- data_ingestion service

---

## 3. Health Context
**Responsibility**
- Evaluate livestock health over time
- Maintain health history

**Owns**
- Health evaluations
- Health state transitions

**Does NOT own**
- Telemetry ingestion
- Incident lifecycle

**Code Mapping**
- management/apps/health/
- ai_decision service (evaluation only)

---

## 4. Incident Context
**Responsibility**
- Represent conditions requiring attention
- Manage incident lifecycle

**Owns**
- Incident entity
- Incident state transitions

**Does NOT own**
- Rule definitions
- Health computation

**Code Mapping**
- management/apps/incidents/

---

## 5. Rules Context
**Responsibility**
- Define deterministic business rules
- Evaluate telemetry against thresholds

**Owns**
- Rule definitions
- Rule evaluation outcomes

**Does NOT own**
- Incident persistence
- Health history

**Code Mapping**
- management/apps/rules/

---

## 6. Monitoring Context
**Responsibility**
- Provide live snapshots
- Support read-only queries

**Owns**
- LiveStatus snapshots

**Does NOT own**
- Persistent data
- Business decisions

**Code Mapping**
- monitoring service (FastAPI)

---

## 7. Edge Context
**Responsibility**
- Discover and manage edge nodes
- Bridge physical devices to cloud services

**Code Mapping**
- edge_controller service
