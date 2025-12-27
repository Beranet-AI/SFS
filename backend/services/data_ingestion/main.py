from fastapi import FastAPI
from backend.services.data_ingestion.api.routes import router

app = FastAPI(title="SFS Data Ingestion")
app.include_router(router)
