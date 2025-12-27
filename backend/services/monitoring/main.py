from fastapi import FastAPI

from backend.services.monitoring.core.config import settings
from backend.services.monitoring.core.lifespan import lifespan
from backend.services.monitoring.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="SFS Monitoring Service",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.include_router(router, prefix=settings.API_PREFIX)
    return app


app = create_app()
