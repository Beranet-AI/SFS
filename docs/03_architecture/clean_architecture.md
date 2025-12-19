# Clean Architecture in SFS

SFS applies Clean Architecture principles at both
**service level** and **system level**.

---

## Layer Definitions

### Domain Layer
- Contains entities, value objects, and domain invariants
- Has no dependency on frameworks or infrastructure

**Example:**
management/apps/incidents/domain/

---

### Application Layer
- Implements use cases
- Coordinates domain objects
- Contains no HTTP, ORM, or framework code

**Example:**
management/apps/incidents/application/

---

### Interface / API Layer
- Exposes use cases via HTTP
- Performs validation and mapping
- Contains no business rules

**Example:**
management/apps/incidents/api/

---

### Infrastructure Layer
- Implements persistence, messaging, external clients
- Is replaceable

**Example:**
management/apps/incidents/infrastructure/

---

## Dependency Rule

Dependencies always point inward:


Violations of this rule are considered architectural defects.

---

## Clean Architecture at System Level

- Django Management = full Clean Architecture stack
- FastAPI services = Application + Infrastructure only
- Frontend = Presentation + Application (hooks)

This asymmetry is intentional and reflects responsibility boundaries.
