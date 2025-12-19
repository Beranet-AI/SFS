# Event Flows Overview

This document describes the major event-driven and request-driven flows
within the Smart Farm System (SFS).

SFS intentionally uses a **hybrid interaction model**:
- Request/Response for commands and queries
- Event-like flows for telemetry and derived decisions

Important distinction:
- An "event" here is a **flow of causality**, not an event-sourcing record.

---

## Core Interaction Categories

1. Telemetry-driven flows
2. Operator-driven flows
3. AI-driven evaluation flows
4. Read-only visualization flows

Each category is documented as a concrete sequence with:
- Trigger
- Participants
- Side effects
- Failure isolation rules
