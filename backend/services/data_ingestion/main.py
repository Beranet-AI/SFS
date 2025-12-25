from fastapi import FastAPI
from data_ingestion.api.routes import router

app = FastAPI(title="SFS Data Ingestion")
app.include_router(router)
