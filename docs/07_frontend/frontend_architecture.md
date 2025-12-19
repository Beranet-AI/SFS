# Frontend Architecture

The SFS frontend is implemented using **Next.js (App Router)** and TypeScript.
It follows the same architectural discipline as the backend:
clear separation between **UI**, **application logic**, and **infrastructure**.

---

## Architectural Goals

- Strong typing via shared DTOs
- No business logic in UI components
- Explicit data-fetching boundaries
- Predictable state flow
- Easy mapping to backend APIs

---

## High-Level Structure


frontend/webapp/src/
├── app/ # Routing & pages
├── ui/ # Presentational components
├── domain/ # Frontend domain models (read-only)
├── application/ # Use-case level logic
├── infrastructure/ # HTTP clients, adapters
└── shared/ # Mirrored shared kernel (DTOs, enums)


---

## Responsibility Boundaries

- UI components: render only
- Hooks / application layer: orchestration
- Infrastructure: API calls, serialization
- Domain: client-side interpretation (never authoritative)

The frontend never:
- Persists business data
- Evaluates business rules
- Bypasses published APIs
