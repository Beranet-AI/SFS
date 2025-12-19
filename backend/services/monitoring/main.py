from fastapi import FastAPI
from monitoring.api.routes import router
from monitoring.core.lifespan import lifespan

app = FastAPI(
    title="SFS Monitoring Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
