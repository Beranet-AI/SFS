from fastapi import FastAPI

from .core.lifespan import lifespan

# routers
from .api.routes.base import router as base_router
from .api.routes.heartbeat import router as heartbeat_router

app = FastAPI(
    title="SFS Edge Controller",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------
# Heartbeat (simple / optional)
# -------------------------
app.include_router(heartbeat_router)

# -------------------------
# Core API (command, telemetry, ...)
# -------------------------
app.include_router(base_router)
