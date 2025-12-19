# State Management

SFS frontend uses **localized and explicit state management**
instead of a global state store.

---

## State Categories

### 1. Server State
- Data fetched from backend APIs
- Examples: incidents, live status, health records

Handled via:
- Custom hooks (e.g. useIncidents, useLiveStatus)
- React state + effects
- Optional caching (future)

---

### 2. UI State
- Modal open/close
- Selected rows
- Filters and sorting

Handled via:
- Component-local state
- Context only when scoped

---

### 3. Derived State
- Severity badges
- Health indicators
- Status colors

Derived at render time from DTOs or domain models.

---

## Explicit Non-Goals

- No Redux or global stores (yet)
- No duplicated backend state
- No hidden side effects

---

## Mapping to Code

- Hooks: `src/application/hooks/`
- UI state: `src/ui/components/`
- API data: `src/infrastructure/http/`
