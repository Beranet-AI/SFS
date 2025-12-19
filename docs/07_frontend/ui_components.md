# UI Components

UI components in SFS are **pure and declarative**.

---

## Component Categories

### 1. Layout Components
- Dashboard layout
- Navigation bars
- Page shells

Path:
src/ui/layout/


---

### 2. Domain Visualization Components
- IncidentList
- LiveStatusPanel
- HealthIndicator

Path:
src/ui/components/


---

### 3. Shared UI Elements
- Buttons
- Badges
- Tables
- Modals

Path:
src/ui/common/


---

## Component Rules

- No API calls inside components
- No direct DTO mutation
- No business decisions
- Props are explicit and typed

---

## Example

```tsx
<IncidentList incidents={incidents} onAcknowledge={ackIncident} />

Components receive intent, not infrastructure.


---

## `docs/07_frontend/routing.md`

```md
# Routing & Navigation

Routing is implemented using **Next.js App Router**.

---

## Route Structure

src/app/
├── layout.tsx
├── page.tsx # Landing / Dashboard
├── incidents/
│ └── page.tsx
├── livestock/
│ └── [id]/
│ └── page.tsx
└── health/
└── [id]/
└── page.tsx


---

## Routing Principles

- Routes represent user intentions
- Dynamic routes map to aggregate identities
- No routing logic inside UI components

---

## Data Fetching

- Data is fetched in hooks
- Pages orchestrate hooks
- Server Components used for layout where applicable

---

## Error Handling

- Route-level error boundaries
- Graceful degradation when APIs fail

---

## Mapping

- Routes → Use Cases
- Use Cases → APIs
- APIs → Backend services
