from fastapi import FastAPI

from .lifespan import lifespan
from .presentation.api.routers.execute_command_router import (
    legacy_router as legacy_execute_command_router,
    router as execute_command_router,
)
from .presentation.api.routers.receive_telemetry_router import (
    router as receive_telemetry_router,
)

app = FastAPI(
    title="SFS Edge Controller",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------
# Core API (command, telemetry, ...)
# -------------------------
app.include_router(execute_command_router)
app.include_router(legacy_execute_command_router)
app.include_router(receive_telemetry_router)
