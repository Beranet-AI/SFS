from fastapi import FastAPI
from .api.routes import register_routes


def create_app() -> FastAPI:
    app = FastAPI(title="data_ingestion")
    register_routes(app)
    return app
