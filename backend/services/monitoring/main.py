from fastapi import FastAPI
from apps.monitoring.api.routes import router

app = FastAPI(title="SFS Monitoring")
app.include_router(router)
