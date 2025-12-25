from fastapi import FastAPI
from edge_controller.api.routes import router

app = FastAPI(title="SFS Edge Controller")
app.include_router(router)
