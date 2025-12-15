from fastapi import FastAPI
from backend.services.alerting.api.events import router as events_router

app = FastAPI(title="Alerting Service")

app.include_router(events_router, prefix="/events")
