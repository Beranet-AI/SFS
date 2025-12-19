# Smart Farm System (SFS) – Documentation

This directory contains the **complete architectural and operational
documentation** for the Smart Farm System (SFS).

The documentation is structured to support:
- Developers
- Architects
- Operators
- Reviewers and auditors

---

## Structure Overview

### 00 – Overview
Vision, scope, glossary, and roadmap.

### 01 – Requirements
Functional and non-functional requirements,
use cases, and constraints.

### 02 – Domain
Domain model, bounded contexts, aggregates, and business rules.

### 03 – Architecture
Clean Architecture, C4 diagrams, deployment, and tech stack.

### 04 – Data
Data model, ERD, migrations, lifecycle, and retention.

### 05 – API
Public API contracts for all services.

### 06 – Interactions
Sequence diagrams and interaction flows.

### 07 – Frontend
Frontend architecture, state management, UI, and routing.

### 08 – Development Guidelines
Coding standards, folder structure, Git strategy, code review checklist.

### 09 – Testing
Test strategy, test cases, and quality metrics.

### 10 – DevOps
Environments, Docker, CI/CD, monitoring, and rollback.

### 11 – Security
Threat model, authentication, data protection, audit logging.

### 12 – Operations
Runbooks, incident response, backup/restore, scaling.

### 13 – Decisions
Architecture Decision Records (ADR).

---

## How to Use This Documentation

- Start with `00_overview/` for context
- Read `02_domain/` before touching business logic
- Use `03_architecture/` and `06_interactions/` for system understanding
- Treat `08_dev_guidelines/` and `09_testing/` as enforceable rules
- Use `12_operations/` for production readiness

---

## Documentation Principles

- Documentation reflects reality, not intention
- Every architectural decision must be traceable
- Diagrams must map to code
- Tests must map to sequences

If documentation and code diverge, **the build must fail**.
