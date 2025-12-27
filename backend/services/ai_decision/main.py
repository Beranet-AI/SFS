
from fastapi import FastAPI
from backend.services.ai_decision.api.routes import router
from backend.services.ai_decision.core.lifespan import lifespan

app = FastAPI(
    title="SFS AI Decision Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


'''
from fastapi import FastAPI
from data_ingestion.api.routes import router

app = FastAPI(title="Data Ingestion Service")

app.include_router(router)

'''