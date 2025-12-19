# Domain Overview

The Smart Farm System (SFS) domain focuses on **livestock health and risk monitoring**
through continuous data acquisition and structured decision-making.

The domain is intentionally split into multiple bounded contexts to:
- Reduce coupling
- Preserve business invariants
- Enable independent evolution of capabilities

At the core of the domain are:
- Livestock as the primary subject
- Telemetry as raw observational data
- Health as evaluated state over time
- Incidents as actionable outcomes

The domain distinguishes clearly between:
- **Facts** (telemetry, timestamps)
- **Evaluations** (health state, predictions)
- **Decisions** (incident creation, resolution)

This separation is fundamental and enforced both in code and architecture.
