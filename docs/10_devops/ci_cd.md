# CI/CD Pipeline

SFS uses CI/CD to enforce architectural integrity and quality.

---

## CI Pipeline (GitHub Actions)

Triggered on:
- Pull Requests
- Merges to main

---

## CI Stages

1. Linting
   - Python (flake8 / black check)
   - TypeScript (eslint)

2. Unit Tests
   - Domain tests
   - Shared kernel tests

3. Integration Tests
   - API tests
   - Service orchestration tests

4. Architecture Guard Tests
   - Dependency direction
   - Forbidden imports

5. Build
   - Docker images
   - Frontend build

---

## CD Pipeline (Planned)

- Manual approval for production
- Zero-downtime deployment
- Automated rollback on failure

---

## Failure Policy

- Any failing stage blocks merge
- No overrides without ADR
