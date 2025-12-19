# Code Review Checklist

This checklist must be applied to every Pull Request.

---

## Architecture

- [ ] Does the change respect bounded contexts?
- [ ] Are dependencies pointing inward?
- [ ] Is the Source of Truth preserved?

---

## Domain Integrity

- [ ] Are domain invariants enforced?
- [ ] Are state transitions explicit?
- [ ] Is ubiquitous language respected?

---

## API Design

- [ ] Are endpoints resource-based?
- [ ] Are actions explicit?
- [ ] Are DTOs used consistently?

---

## Testing

- [ ] Are new behaviors covered by tests?
- [ ] Do tests reflect sequence diagrams?
- [ ] Are architecture guard tests still passing?

---

## Frontend

- [ ] No API calls in UI components
- [ ] Hooks represent clear use cases
- [ ] Shared DTOs used correctly

---

## Documentation

- [ ] Relevant docs updated
- [ ] ADR added if architectural decision made

---

## Final Gate

If any item fails:
- PR must not be merged
- Or justification must be documented
