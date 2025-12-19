# Data Model Overview

SFS data model is designed around a **single authoritative data store**
owned by the Management service.

The model separates:
- **Raw facts** (telemetry)
- **Derived evaluations** (health)
- **Decisions** (incidents)
- **Read models** (live status)

This separation prevents data coupling and enables independent evolution.

---

## Core Data Categories

### 1. Master Data
- Livestock
- Farm
- Device

Characteristics:
- Low change frequency
- Strong identity
- Owned by domain aggregates

---

### 2. Observational Data
- Telemetry records

Characteristics:
- High volume
- Immutable
- Time-series oriented

---

### 3. Evaluated Data
- Health evaluations
- AI predictions

Characteristics:
- Derived from telemetry
- Versioned over time
- Traceable to source data

---

### 4. Decision Data
- Incidents
- Incident state transitions

Characteristics:
- Explicit lifecycle
- Auditable
- Human-interaction driven

---

## Ownership Rules

- Only Management service persists data
- FastAPI services may cache or compute but never own
- Frontend never persists data
