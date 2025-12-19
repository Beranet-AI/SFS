from fastapi import FastAPI
from data_ingestion.api.routes import router
from data_ingestion.core.lifespan import lifespan

app = FastAPI(
    title="SFS Data Ingestion Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
