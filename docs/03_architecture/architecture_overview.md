# Architecture Overview

Smart Farm System (SFS) is designed as a **modular, service-oriented system**
that combines a strong domain core with scalable, stateless services.

The architecture follows these principles:

1. **Single Source of Truth**
   - All persistent business data is owned by the Management service (Django).

2. **Separation of Concerns**
   - Domain logic, orchestration, and infrastructure are clearly separated.

3. **Bounded Context Isolation**
   - Each service corresponds to a well-defined bounded context.

4. **Read / Write Separation**
   - Command operations affect the domain.
   - Query operations are optimized and isolated.

5. **Evolutionary Architecture**
   - Rule-based logic can evolve into AI-driven decision-making
     without breaking core contracts.

At a high level, SFS consists of:
- A central Management service
- Multiple FastAPI services for ingestion, monitoring, and intelligence
- A web-based frontend
- Edge components bridging physical devices

This architecture is intentionally biased toward **clarity, traceability,
and long-term maintainability** over short-term convenience.
