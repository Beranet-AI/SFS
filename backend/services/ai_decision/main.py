from fastapi import FastAPI
from ai_decision.api.routes import router
from ai_decision.core.lifespan import lifespan

app = FastAPI(
    title="SFS AI Decision Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
