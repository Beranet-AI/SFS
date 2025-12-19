# Coding Standards

This document defines mandatory coding standards for the SFS project.

These rules are not stylistic preferences.
They are architectural constraints.

---

## General Principles

- Code must reflect the domain language
- Explicit is better than implicit
- Errors must be handled consciously
- Side effects must be visible

---

## Python (Backend)

### Structure
- One responsibility per module
- Files larger than ~300 lines require justification

### Naming
- snake_case for functions and variables
- PascalCase for classes
- Domain terms must match ubiquitous language

### Imports
- No wildcard imports
- Domain layer must not import framework code

### Error Handling
- Domain errors are explicit exceptions
- API layer maps exceptions to HTTP responses

---

## TypeScript (Frontend)

### Typing
- `any` is forbidden
- Shared DTOs must be imported from `shared/`

### Components
- Components are pure
- Side effects only in hooks

### Hooks
- One hook = one use case
- Hooks return data + intent handlers

---

## Formatting

- Python: Black-compatible formatting
- TypeScript: Prettier
- Lint errors block merge

---

## Forbidden Practices

- Business logic in controllers
- ORM access outside Management
- API calls inside UI components
