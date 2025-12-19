from fastapi import FastAPI
from edge_controller.api.routes import router
from edge_controller.core.lifespan import lifespan

app = FastAPI(
    title="SFS Edge Controller",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
