# Folder Structure Guidelines

Folder structure reflects architecture.
Violating it means violating design.

---

## Backend

backend/
├── services/
│ ├── management/
│ │ └── apps/
│ │ └── <context>/
│ │ ├── domain/
│ │ ├── application/
│ │ ├── api/
│ │ └── infrastructure/
│ ├── data_ingestion/
│ ├── monitoring/
│ ├── ai_decision/
│ └── edge_controller/
└── shared/


Rules:
- Domain code only inside `domain/`
- No cross-context imports
- FastAPI services never contain domain entities

---

## Frontend

frontend/webapp/src/
├── app/
├── ui/
├── application/
├── infrastructure/
├── domain/
└── shared/


Rules:
- UI does not fetch data
- Infrastructure does not contain UI logic
- Domain is read-only representation

---

## Tests

tests/
├── unit/
├── integration/
├── architecture/
└── system/


Rules:
- Architecture tests block merge
- Integration tests mirror sequence diagrams
